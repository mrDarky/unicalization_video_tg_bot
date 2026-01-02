"""
Test script for admin panel features:
- Authentication
- Tariff Plans
- Video Limitations
"""
import asyncio
from database.database import async_session_maker, init_db
from database.crud import (
    create_tariff_plan,
    get_tariff_plan,
    check_user_can_process_videos,
    get_or_create_user,
    assign_tariff_plan_to_user,
    increment_daily_usage,
    get_user_daily_usage
)


async def test_database_models():
    """Test that new models exist"""
    print("Testing database models...")
    
    from database.models import TariffPlan, DailyVideoUsage, User
    from sqlalchemy import inspect
    
    # Check TariffPlan model
    mapper = inspect(TariffPlan)
    columns = [col.key for col in mapper.columns]
    assert 'name' in columns
    assert 'videos_per_day' in columns
    assert 'videos_per_order' in columns
    assert 'price' in columns
    print("  ✓ TariffPlan model has required columns")
    
    # Check DailyVideoUsage model
    mapper = inspect(DailyVideoUsage)
    columns = [col.key for col in mapper.columns]
    assert 'user_id' in columns
    assert 'date' in columns
    assert 'video_count' in columns
    print("  ✓ DailyVideoUsage model has required columns")
    
    # Check User model has tariff_plan_id
    mapper = inspect(User)
    columns = [col.key for col in mapper.columns]
    assert 'tariff_plan_id' in columns
    print("  ✓ User model has tariff_plan_id column")
    
    print("✅ Database models test passed!")


async def test_tariff_plan_crud():
    """Test tariff plan CRUD operations"""
    print("Testing tariff plan CRUD...")
    
    async with async_session_maker() as session:
        # Create
        plan = await create_tariff_plan(
            session,
            name='Test Plan',
            description='Test description',
            videos_per_day=15,
            videos_per_order=5,
            price=9.99
        )
        assert plan.name == 'Test Plan'
        assert plan.videos_per_day == 15
        assert plan.videos_per_order == 5
        print("  ✓ Tariff plan created successfully")
        
        # Read
        fetched_plan = await get_tariff_plan(session, plan.id)
        assert fetched_plan is not None
        assert fetched_plan.name == 'Test Plan'
        print("  ✓ Tariff plan fetched successfully")
    
    print("✅ Tariff plan CRUD test passed!")


async def test_limit_checking():
    """Test video limit checking"""
    print("Testing video limit checking...")
    
    async with async_session_maker() as session:
        # Create a test user
        user = await get_or_create_user(
            session,
            telegram_id=99999,
            username='limit_test_user'
        )
        
        # Create a tariff plan with specific limits
        plan = await create_tariff_plan(
            session,
            name='Limited Plan',
            videos_per_day=5,
            videos_per_order=2,
            price=0.0
        )
        
        # Assign plan to user
        await assign_tariff_plan_to_user(session, user.id, plan.id)
        print("  ✓ User assigned to tariff plan")
        
        # Test order limit - should pass
        can_process, error = await check_user_can_process_videos(session, user.id, 2)
        assert can_process is True
        print("  ✓ Order limit check passed (2 videos allowed)")
        
        # Test order limit - should fail
        can_process, error = await check_user_can_process_videos(session, user.id, 3)
        assert can_process is False
        assert 'Order limit exceeded' in error
        print("  ✓ Order limit check passed (3 videos blocked)")
        
        # Test daily limit - process some videos
        await increment_daily_usage(session, user.id, 2)
        usage = await get_user_daily_usage(session, user.id)
        assert usage == 2
        print("  ✓ Daily usage incremented correctly")
        
        # Test daily limit - should pass (3 more allowed)
        can_process, error = await check_user_can_process_videos(session, user.id, 2)
        assert can_process is True
        print("  ✓ Daily limit check passed (2 more videos allowed)")
        
        # Test daily limit - should fail (only 3 remaining, requesting 4)
        can_process, error = await check_user_can_process_videos(session, user.id, 2)
        # First increment to 4 total
        await increment_daily_usage(session, user.id, 2)
        can_process, error = await check_user_can_process_videos(session, user.id, 2)
        assert can_process is False
        assert 'Daily limit exceeded' in error
        print("  ✓ Daily limit check passed (limit reached)")
    
    print("✅ Limit checking test passed!")


async def test_authentication_setup():
    """Test that authentication module is set up correctly"""
    print("Testing authentication setup...")
    
    from api.auth import (
        verify_password,
        get_password_hash,
        create_access_token,
        verify_token
    )
    
    # Test password hashing
    password = "testpassword123"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False
    print("  ✓ Password hashing works correctly")
    
    # Test JWT token creation and verification
    token = create_access_token(data={"sub": "admin"})
    assert token is not None
    payload = verify_token(token)
    assert payload is not None
    assert payload['sub'] == 'admin'
    print("  ✓ JWT token creation and verification works")
    
    print("✅ Authentication setup test passed!")


async def main():
    print("=" * 50)
    print("Admin Panel Features Test Suite")
    print("=" * 50)
    print()
    
    try:
        # Initialize database
        await init_db()
        print("✅ Database initialized\n")
        
        await test_database_models()
        print()
        
        await test_tariff_plan_crud()
        print()
        
        await test_limit_checking()
        print()
        
        await test_authentication_setup()
        print()
        
        print("=" * 50)
        print("✅ ALL TESTS PASSED!")
        print("=" * 50)
    except AssertionError as e:
        print()
        print("=" * 50)
        print(f"❌ TEST FAILED: {e}")
        print("=" * 50)
        exit(1)
    except Exception as e:
        print()
        print("=" * 50)
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 50)
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
