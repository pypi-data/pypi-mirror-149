#!/usr/bin/env python3
import subprocess
import time
import math
from PIL import Image
from pathlib import Path
import tempfile
import imagehash

from . import keycode_enum

# https://github.com/0187773933/ADBWrapper/blob/master/v1/wrapper/wrapper.go
class ADBWrapper:

	def __init__( self , options={} ):
		self.options = options
		self.connect()
		self.turn_on_screen()

	def sleep( self , milliseconds ):
		time.sleep( milliseconds )

	def exec( self , bash_command ):
		try:
			return subprocess.getoutput( bash_command )
		except Exception as e:
			print( e )
			return False

	def connect( self ):
		result = self.exec( f"adb connect {self.options['ip']}:{self.options['port']}" )
		print( result )

	def press_key( self , key_code ):
		result = self.exec( f"adb shell input keyevent {key_code}" )
		print( result )

	def press_key_sequence( self , key_sequence ):
		key_sequence = " ".join( [ str( x ) for x in key_sequence ] )
		result = self.exec( f"adb shell input keyevent {key_sequence}" )
		print( result )

	def press_keycode( self , key_code ):
		if keycode_enum.KEYCODES[ key_code ] == False:
			print( "keycode name not found in enum" )
			return False
		self.press_key( keycode_enum.KEYCODES[ key_code ] )

	# https://github.com/ceberous/ShzmTwitchBot/blob/master/main.js#L40=
	def tap( self , x , y ):
		result = self.exec( f"adb shell input tap {x} {y}" )
		print( result )

	def get_screen_power_state( self ):
		try:
			# result = self.exec( 'adb shell dumpsys input_method | grep -c "mScreenOn=true"' )
			result = self.exec( 'adb shell dumpsys power | grep mWakefulness=' )
			result = result.split( "=" )[ 1 ].strip()
			self.screen_power_state = result
		except Exception as e:
			print( e )
			self.screen_power_state = False

	def turn_on_screen( self ):
		self.get_screen_power_state()
		if self.screen_power_state != "Awake":
			self.press_key( 26 )
			self.get_screen_power_state()
		print( self.screen_power_state )

	def open_uri( self , uri ):
		result = self.exec( f"adb shell am start -a android.intent.action.VIEW -d {uri}" )
		print( result )

	def get_status( self ):

		# 1.) Parse Window Stack
		window_stack = self.exec( f"adb shell dumpsys window windows" )
		windows = window_stack.split( "Window #" )
		windows = windows[ 1 : ] # remove WINDOW MANAGER Preamble
		parsed_windows = []
		for window_index , window in enumerate( windows ):
			window_data_lines = window.split( "\n" )
			parsed_window = { "window_index": window_index }
			parsed_window[ "title" ] = window_data_lines[ 0 ].split( " " )[ -1 ].split( "}" )[ 0 ]
			for window_data_line_index , window_data_line in enumerate( window_data_lines ):
				# print( f"Window # {window_index} === Line # {window_data_line_index} === {window_data_line}" )
				if "mFrame=" in window_data_line:
					parsed_window[ "frame_geometry" ] = window_data_line.split( "mFrame=" )[ 1 ].split( " " )[ 0 ]
				elif "isOnScreen=" in window_data_line:
					parsed_window[ "is_on_screen" ] = window_data_line.split( "isOnScreen=" )[ 1 ]
				elif "isVisible=" in window_data_line:
					parsed_window[ "is_visible" ] = window_data_line.split( "isVisible=" )[ 1 ]
			parsed_windows.append( parsed_window )
		parsed_windows = sorted( parsed_windows , key=lambda x: x[ "is_visible" ] , reverse=True )
		self.window_stack = parsed_windows

		# 2.) Parse Media Session
		media_session = self.exec( f"adb shell dumpsys media_session" )
		media_session = media_session.split( "Sessions Stack" )[ 1 ]

		parsed_sessions = []

		media_sessions = media_session.split( "\n\n" )
		now_playing = media_sessions[ -1 ]
		if "packages=" in now_playing:
			now_playing = now_playing.split( "packages=" )[ 1 ]
		media_sessions = media_sessions[ 0 : -1 ]
		for media_session_index , media_session in enumerate( media_sessions ):
			# print( f"{index} === {media_session}" )
			media_session_lines = media_session.split( "\n" )
			parsed_session = {}
			if media_session_index == 0:
				media_session_lines = media_session_lines[ 1 : ]
			parsed_session[ "title_info" ] = media_session_lines[ 0 ].split( " " )[ 0 : -1 ]
			parsed_session[ "title_info" ] = [ x for x in parsed_session[ "title_info" ] if x ]
			for media_session_line_index , media_session_line in enumerate( media_session_lines ):
				# print( f"Media Session === {media_session_index} === {media_session_line_index} === {media_session_line.strip()}" )
				if "package=" in media_session_line:
					parsed_session[ "app_name" ] = media_session_line.split( "package=" )[ 1 ]
				elif "active=" in media_session_line:
					parsed_session[ "active" ] = media_session_line.split( "active=" )[ 1 ]
				elif "PlaybackState {" in media_session_line:
					state = media_session_line.split( "PlaybackState {" )[ 1 ].split( "}" )[ 0 ].split( "," )
					parsed_session[ "state" ] = {
						"state": state[ 0 ].split( "=" )[ 1 ] ,
						"position": state[ 1 ].split( "=" )[ 1 ] ,
						"buffered_position": state[ 2 ].split( "=" )[ 1 ] ,
						"speed": state[ 3 ].split( "=" )[ 1 ] ,
						"updated": state[ 4 ].split( "=" )[ 1 ] ,
						"actions": state[ 5 ].split( "=" )[ 1 ] ,
						"custom_actions": state[ 6 ].split( "=" )[ 1 ] ,
						"active_item_id": state[ 7 ].split( "=" )[ 1 ] ,
						"error": state[ 8 ].split( "=" )[ 1 ] ,
					}
				elif "volumeType=" in media_session_line:
					volume_type = media_session_line.split( "volumeType=" )[ 1 ].split( "," )
					parsed_session[ "volume" ] = {
						"type": volume_type[ 0 ] ,
						"control_type": volume_type[ 1 ].split( "=" )[ 1 ] ,
						"max": volume_type[ 2 ].split( "=" )[ 1 ] ,
						"current": volume_type[ 3 ].split( "=" )[ 1 ] ,
					}
				elif "metadata:" in media_session_line:
					meta_data = media_session_line.split( "metadata:" )[ 1 ]
					description = meta_data.split( "description=" )[ 1 ]
					if description.endswith( ", null" ):
						description = description.split( ", null" )[ 0 ]
					parsed_session[ "meta_data" ] = {
						"size": meta_data.split( "size=" )[ 1 ].split( ", description=" )[ 0 ] ,
						"description": description
					}
			parsed_sessions.append( parsed_session )
		self.now_playing = {
			"now_playing_app": now_playing ,
			"sessions": parsed_sessions ,
		}
		return {
			"now_playing": self.now_playing ,
			"window_stack": self.window_stack
		}

	def take_screen_shot( self ):
		try:
			with tempfile.TemporaryDirectory() as temp_dir:
				temp_dir_posix = Path( temp_dir )
				with tempfile.NamedTemporaryFile( suffix='.png' , prefix=temp_dir ) as tf:
					temp_file_path = temp_dir_posix.joinpath( tf.name )
					self.exec( f"adb exec-out screencap -p > {str( temp_file_path )}" )
					self.screen_shot = Image.open( str( temp_file_path ) )
		except Exception as e:
			print( e )
			return False

	# https://github.com/JohannesBuchner/imagehash
	def screen_difference_to_image( self , image_path ):
		try:
			with tempfile.TemporaryDirectory() as temp_dir:
				temp_dir_posix = Path( temp_dir )
				with tempfile.NamedTemporaryFile( suffix='.png' , prefix=temp_dir ) as tf:
					temp_file_path = temp_dir_posix.joinpath( tf.name )
					self.exec( f"adb exec-out screencap -p > {str( temp_file_path )}" )
					screen_shot = Image.open( str( temp_file_path ) )
					compared_image = Image.open( str( image_path ) )
					screen_shot_hash = imagehash.phash( screen_shot )
					compared_image_hash = imagehash.phash( compared_image )
					difference = ( screen_shot_hash - compared_image_hash )
					return difference
		except Exception as e:
			print( e )
			return False
