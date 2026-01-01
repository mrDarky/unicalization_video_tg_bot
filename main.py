#!/usr/bin/env python3
"""
Video Unicalization - Main Launcher
Run as Telegram Bot or Desktop Application
"""

import sys
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description='Video Unicalization - Run as bot or desktop application',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --mode bot          # Run as Telegram bot
  python main.py --mode desktop      # Run as desktop application
  python main.py --mode api          # Run API server only
        """
    )
    
    parser.add_argument(
        '--mode',
        choices=['bot', 'desktop', 'api'],
        default='desktop',
        help='Run mode: bot (Telegram bot), desktop (GUI app), or api (API server)'
    )
    
    args = parser.parse_args()
    
    try:
        if args.mode == 'bot':
            logger.info("Starting Telegram Bot mode...")
            from bot_main import main as bot_main
            import asyncio
            asyncio.run(bot_main())
            
        elif args.mode == 'desktop':
            logger.info("Starting Desktop Application mode...")
            from desktop_app import run_desktop_app
            run_desktop_app()
            
        elif args.mode == 'api':
            logger.info("Starting API Server mode...")
            from api_main import main as api_main
            import asyncio
            asyncio.run(api_main())
            
    except KeyboardInterrupt:
        logger.info(f"{args.mode.capitalize()} mode stopped by user")
    except Exception as e:
        logger.error(f"Error running in {args.mode} mode: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
