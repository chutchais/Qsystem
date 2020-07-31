# Create your tasks here
# from __future__ import absolute_import, unicode_literals
# from celery import shared_task
# from .models import Job


# @shared_task
# def add(x, y):
#     return x + y


# @shared_task
# def mul(x, y):
#     return x * y


# @shared_task
# def xsum(numbers):
#     return sum(numbers)
# from django.conf import settings
import os

# @shared_task
def play_call_sound(job_q_number,counter_number,job_prefix):
	# job = Job.objects.get(pk=job_pk)
	
	cwd = os.getcwd()
	sound_root_path = '%s\\sound\\' % cwd #f"{cwd}\\sound\\"
	# print (sound_root_path)
	try:
		from pathlib import Path
		file_wav = 'welcomeNumber.wav'
		file_wav = sound_root_path + file_wav
		sound_file = Path(file_wav)
		from playsound import playsound
		if sound_file.exists():
			playsound(file_wav) #Welcome sound
			# playsound(sound_root_path + '%s.wav' % job.queue_number )
			playsound(sound_root_path + '%s.wav' % job_prefix)

			play_number_sound(job_q_number) # Jon Number
			playsound(sound_root_path + 'counter.wav')#At counter

			playsound(sound_root_path + '%s.wav' % counter_number)#Counter number
			#playsound('c:\\users\\gate\\sounds\\truck2.wav')
		else :
			print ('Not found sounds/X.wav file')
	except:
		print ('Error on play_call_sound')

def play_number_sound(job):
	import time
	from playsound import playsound
	cwd = os.getcwd()
	sound_root_path = '%s\\sound\\' % cwd #f"{cwd}\\sound\\"
	# sound_root_path = 'd:\\qsystem\\media\\sound\\'
	# job_number = job.queue_number
	job_number = job
	try:
		if job_number < 11 :		
			playsound(sound_root_path + '%s.wav' % job_number )
		if job_number >= 11 and job_number < 100  :
			play_ten_sound(job_number)
		if job_number >= 100:
			play_hundred_sound(job_number)

	except:
		print ('Error on play_number_sound')

def play_ten_sound(q_number):
	import time
	from playsound import playsound
	cwd = os.getcwd()
	sound_root_path = '%s\\sound\\' % cwd #f"{cwd}\\sound\\"
	# sound_root_path = 'd:\\qsystem\\media\\sound\\'
	job_number = q_number
	try:
		if job_number < 11 :		
			playsound(sound_root_path + '%s.wav' % job_number )
		if job_number >= 11 and job_number < 100  :
			# print(job_number)
			last_digit = int(str(job_number)[-1])
			ten_digit  = int(str(job_number)[0:1])*10
			# print(ten_digit ,last_digit)
			playsound(sound_root_path + '%s.wav' % ten_digit )
			time.sleep(0.1)
			if last_digit == 1:
				playsound(sound_root_path + '_1.wav' )
			else :
				playsound(sound_root_path + '%s.wav' % last_digit )

	except:
		print ('Error on play_ten_sound')

def play_hundred_sound(q_number):
	import time
	from playsound import playsound
	cwd = os.getcwd()
	sound_root_path = '%s\\sound\\' % cwd #f"{cwd}\\sound\\"
	# sound_root_path = 'd:\\qsystem\\media\\sound\\'
	job_number = q_number
	try:
		last_digit = int(str(job_number)[-1])
		ten_digit  = int(str(job_number)[1:3])
		hundred_digit  = int(str(job_number)[0:1])
		# print(hundred_digit)
		# print(ten_digit ,last_digit)
		playsound(sound_root_path + '%s.wav' % hundred_digit )
		playsound(sound_root_path + '100.wav' )
		# time.sleep(0.1)
		if ten_digit > 0:
			play_ten_sound(ten_digit)

	except:
		print ('Error on play_hundred_sound')