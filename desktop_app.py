"""
Kivy Desktop Application for Video Unicalization
Multiplatform video processing desktop application
"""

import os
import asyncio
from threading import Thread
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.clock import Clock
from config import settings
from utils.video_processing import (
    get_video_info,
    change_video_speed,
    scale_video,
    apply_filter,
    crop_video,
    rotate_video,
    add_text_to_video,
    trim_video,
    merge_videos,
    generate_filename
)

# Set window size
Window.size = (900, 700)


class VideoProcessorApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_video = None
        self.selected_video2 = None
        self.processing_mode = "single"
        self.modifications = []
        
    def build(self):
        self.title = "Video Unicalization - Desktop App"
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text='Video Unicalization Tool',
            size_hint=(1, 0.1),
            font_size='24sp',
            bold=True
        )
        main_layout.add_widget(header)
        
        # Mode selection
        mode_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        mode_label = Label(text='Processing Mode:', size_hint=(0.3, 1))
        self.mode_spinner = Spinner(
            text='Single Video',
            values=('Single Video', 'Merge Two Videos'),
            size_hint=(0.7, 1)
        )
        self.mode_spinner.bind(text=self.on_mode_change)
        mode_layout.add_widget(mode_label)
        mode_layout.add_widget(self.mode_spinner)
        main_layout.add_widget(mode_layout)
        
        # Video selection
        video_select_layout = BoxLayout(size_hint=(1, 0.15), spacing=10)
        self.video_label = Label(
            text='No video selected',
            size_hint=(0.6, 1)
        )
        select_btn = Button(
            text='Select Video',
            size_hint=(0.2, 1),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        select_btn.bind(on_press=self.show_file_chooser)
        
        self.video2_btn = Button(
            text='Select Video 2',
            size_hint=(0.2, 1),
            background_color=(0.2, 0.6, 0.8, 1),
            disabled=True
        )
        self.video2_btn.bind(on_press=lambda x: self.show_file_chooser(x, video2=True))
        
        video_select_layout.add_widget(self.video_label)
        video_select_layout.add_widget(select_btn)
        video_select_layout.add_widget(self.video2_btn)
        main_layout.add_widget(video_select_layout)
        
        # Processing options (scrollable)
        options_scroll = ScrollView(size_hint=(1, 0.4))
        self.options_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.options_layout.bind(minimum_height=self.options_layout.setter('height'))
        
        # Speed control
        self.add_option_row('Speed:', ['0.5x', '0.75x', '1.0x', '1.25x', '1.5x', '2.0x'], 'speed')
        
        # Scale control
        self.add_option_row('Scale:', ['Original', '1920x1080', '1280x720', '854x480', '640x360'], 'scale')
        
        # Filters
        self.add_option_row('Filter:', [
            'None', 'Hue', 'Brightness', 'Contrast', 'Saturation',
            'Blur', 'Sharpen', 'Grayscale', 'Sepia', 'Negative', 'Noise'
        ], 'filter')
        
        # Rotation
        self.add_option_row('Rotate:', ['0°', '90°', '180°', '270°'], 'rotate')
        
        # Text overlay
        text_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        text_layout.add_widget(Label(text='Add Text:', size_hint=(0.3, 1)))
        self.text_input = TextInput(
            hint_text='Enter text to overlay',
            multiline=False,
            size_hint=(0.7, 1)
        )
        text_layout.add_widget(self.text_input)
        self.options_layout.add_widget(text_layout)
        
        # Merge layout (for two video mode)
        self.merge_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        self.merge_layout.add_widget(Label(text='Merge Layout:', size_hint=(0.3, 1)))
        self.merge_spinner = Spinner(
            text='Horizontal',
            values=('Horizontal', 'Vertical', 'Sequential'),
            size_hint=(0.7, 1)
        )
        self.merge_layout.add_widget(self.merge_spinner)
        self.merge_layout.opacity = 0
        self.merge_layout.disabled = True
        self.options_layout.add_widget(self.merge_layout)
        
        options_scroll.add_widget(self.options_layout)
        main_layout.add_widget(options_scroll)
        
        # Progress bar
        self.progress_bar = ProgressBar(max=100, size_hint=(1, 0.05))
        main_layout.add_widget(self.progress_bar)
        
        # Status label
        self.status_label = Label(
            text='Ready to process',
            size_hint=(1, 0.08),
            color=(0.8, 0.8, 0.8, 1)
        )
        main_layout.add_widget(self.status_label)
        
        # Process button
        process_btn = Button(
            text='Process Video',
            size_hint=(1, 0.12),
            background_color=(0.2, 0.8, 0.2, 1),
            font_size='18sp',
            bold=True
        )
        process_btn.bind(on_press=self.process_video)
        main_layout.add_widget(process_btn)
        
        return main_layout
    
    def add_option_row(self, label_text, values, option_type):
        """Add a row with label and spinner for options"""
        layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        layout.add_widget(Label(text=label_text, size_hint=(0.3, 1)))
        spinner = Spinner(
            text=values[0] if 'Original' not in values and 'None' not in values and '1.0x' not in values else 
                 ('Original' if 'Original' in values else ('None' if 'None' in values else '1.0x')),
            values=values,
            size_hint=(0.7, 1)
        )
        spinner.option_type = option_type
        layout.add_widget(spinner)
        self.options_layout.add_widget(layout)
        return spinner
    
    def on_mode_change(self, spinner, text):
        """Handle mode change"""
        if text == 'Merge Two Videos':
            self.processing_mode = "merge"
            self.video2_btn.disabled = False
            self.merge_layout.opacity = 1
            self.merge_layout.disabled = False
        else:
            self.processing_mode = "single"
            self.video2_btn.disabled = True
            self.merge_layout.opacity = 0
            self.merge_layout.disabled = True
            self.selected_video2 = None
    
    def show_file_chooser(self, instance, video2=False):
        """Show file chooser dialog"""
        content = BoxLayout(orientation='vertical')
        
        # File chooser
        file_chooser = FileChooserListView(
            filters=['*.mp4', '*.avi', '*.mov', '*.mkv', '*.flv', '*.wmv'],
            path=os.path.expanduser('~')
        )
        content.add_widget(file_chooser)
        
        # Buttons
        btn_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)
        select_btn = Button(text='Select')
        cancel_btn = Button(text='Cancel')
        btn_layout.add_widget(select_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        # Create popup
        popup = Popup(
            title='Select Video File' + (' 2' if video2 else ''),
            content=content,
            size_hint=(0.9, 0.9)
        )
        
        def on_select(instance):
            if file_chooser.selection:
                selected_file = file_chooser.selection[0]
                if video2:
                    self.selected_video2 = selected_file
                    self.update_video_label()
                else:
                    self.selected_video = selected_file
                    self.update_video_label()
            popup.dismiss()
        
        select_btn.bind(on_press=on_select)
        cancel_btn.bind(on_press=popup.dismiss)
        
        popup.open()
    
    def update_video_label(self):
        """Update video label with selected files"""
        if self.processing_mode == "single":
            if self.selected_video:
                self.video_label.text = f'Selected: {os.path.basename(self.selected_video)}'
            else:
                self.video_label.text = 'No video selected'
        else:
            video1_name = os.path.basename(self.selected_video) if self.selected_video else 'None'
            video2_name = os.path.basename(self.selected_video2) if self.selected_video2 else 'None'
            self.video_label.text = f'Video 1: {video1_name} | Video 2: {video2_name}'
    
    def show_error(self, message):
        """Show error popup"""
        popup = Popup(
            title='Error',
            content=Label(text=message),
            size_hint=(0.6, 0.3)
        )
        popup.open()
    
    def show_success(self, output_path):
        """Show success popup with output file location"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text='Video processed successfully!'))
        content.add_widget(Label(text=f'Saved to:\n{output_path}'))
        
        close_btn = Button(text='OK', size_hint=(1, 0.3))
        
        popup = Popup(
            title='Success',
            content=content,
            size_hint=(0.7, 0.4)
        )
        
        close_btn.bind(on_press=popup.dismiss)
        content.add_widget(close_btn)
        popup.open()
    
    def process_video(self, instance):
        """Process video with selected options"""
        if not self.selected_video:
            self.show_error('Please select a video first!')
            return
        
        if self.processing_mode == "merge" and not self.selected_video2:
            self.show_error('Please select second video for merge mode!')
            return
        
        # Disable button during processing
        instance.disabled = True
        self.status_label.text = 'Processing...'
        self.progress_bar.value = 0
        
        # Start processing in background thread
        thread = Thread(target=self.process_video_thread, args=(instance,))
        thread.daemon = True
        thread.start()
    
    def process_video_thread(self, button):
        """Background thread for video processing"""
        try:
            # Create event loop for async functions
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Create output directory
            os.makedirs(settings.PROCESSED_VIDEO_DIR, exist_ok=True)
            os.makedirs(settings.TEMP_VIDEO_DIR, exist_ok=True)
            
            if self.processing_mode == "merge":
                result = loop.run_until_complete(self.process_merge_videos())
            else:
                result = loop.run_until_complete(self.process_single_video())
            
            loop.close()
            
            # Update UI on main thread
            if result['success']:
                Clock.schedule_once(lambda dt: self.on_processing_complete(button, result['output_path']), 0)
            else:
                Clock.schedule_once(lambda dt: self.on_processing_error(button, result['error']), 0)
                
        except Exception as e:
            Clock.schedule_once(lambda dt: self.on_processing_error(button, str(e)), 0)
    
    async def process_single_video(self):
        """Process single video with modifications"""
        try:
            input_path = self.selected_video
            current_path = input_path
            temp_files = []
            
            # Update progress
            Clock.schedule_once(lambda dt: setattr(self.progress_bar, 'value', 10), 0)
            
            # Get spinners from options layout
            spinners = []
            for child in self.options_layout.children:
                if isinstance(child, BoxLayout):
                    for widget in child.children:
                        if isinstance(widget, Spinner) and hasattr(widget, 'option_type'):
                            spinners.append(widget)
            
            progress_step = 80 / max(len(spinners) + 1, 1)
            current_progress = 10
            
            # Apply modifications
            for spinner in reversed(spinners):
                option_type = spinner.option_type
                value = spinner.text
                
                # Skip if default value
                if value in ['Original', 'None', '0°', '1.0x']:
                    continue
                
                output_path = os.path.join(settings.TEMP_VIDEO_DIR, generate_filename())
                temp_files.append(output_path)
                
                Clock.schedule_once(
                    lambda dt, t=option_type: setattr(self.status_label, 'text', f'Applying {t}...'), 0
                )
                
                if option_type == 'speed':
                    speed = float(value.replace('x', ''))
                    await change_video_speed(current_path, output_path, speed)
                elif option_type == 'scale':
                    width, height = map(int, value.split('x'))
                    await scale_video(current_path, output_path, width, height)
                elif option_type == 'filter':
                    await apply_filter(current_path, output_path, value.lower())
                elif option_type == 'rotate':
                    angle = int(value.replace('°', ''))
                    if angle > 0:
                        await rotate_video(current_path, output_path, angle)
                    else:
                        continue
                
                current_path = output_path
                current_progress += progress_step
                Clock.schedule_once(lambda dt, p=current_progress: setattr(self.progress_bar, 'value', p), 0)
            
            # Apply text if provided
            if self.text_input.text.strip():
                output_path = os.path.join(settings.TEMP_VIDEO_DIR, generate_filename())
                temp_files.append(output_path)
                Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Adding text overlay...'), 0)
                await add_text_to_video(current_path, output_path, self.text_input.text.strip())
                current_path = output_path
            
            # Copy to final destination
            final_output = os.path.join(settings.PROCESSED_VIDEO_DIR, generate_filename())
            if current_path == input_path:
                # No modifications, just copy
                import shutil
                shutil.copy(input_path, final_output)
            else:
                import shutil
                shutil.move(current_path, final_output)
            
            # Clean up temp files
            for temp_file in temp_files:
                if os.path.exists(temp_file) and temp_file != current_path:
                    os.remove(temp_file)
            
            Clock.schedule_once(lambda dt: setattr(self.progress_bar, 'value', 100), 0)
            return {'success': True, 'output_path': final_output}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def process_merge_videos(self):
        """Process and merge two videos"""
        try:
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', 'Merging videos...'), 0)
            Clock.schedule_once(lambda dt: setattr(self.progress_bar, 'value', 30), 0)
            
            # Get merge layout
            layout_map = {
                'Horizontal': 'horizontal',
                'Vertical': 'vertical',
                'Sequential': 'sequential'
            }
            layout = layout_map.get(self.merge_spinner.text, 'horizontal')
            
            # Merge videos
            output_path = os.path.join(settings.PROCESSED_VIDEO_DIR, generate_filename())
            Clock.schedule_once(lambda dt: setattr(self.progress_bar, 'value', 70), 0)
            
            success = await merge_videos(
                self.selected_video,
                self.selected_video2,
                output_path,
                layout
            )
            
            Clock.schedule_once(lambda dt: setattr(self.progress_bar, 'value', 100), 0)
            
            if success:
                return {'success': True, 'output_path': output_path}
            else:
                return {'success': False, 'error': 'Failed to merge videos'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def on_processing_complete(self, button, output_path):
        """Handle successful processing"""
        button.disabled = False
        self.status_label.text = 'Processing complete!'
        self.show_success(output_path)
    
    def on_processing_error(self, button, error):
        """Handle processing error"""
        button.disabled = False
        self.status_label.text = 'Processing failed!'
        self.progress_bar.value = 0
        self.show_error(f'Processing error:\n{error}')


def run_desktop_app():
    """Run the desktop application"""
    app = VideoProcessorApp()
    app.run()


if __name__ == '__main__':
    run_desktop_app()
