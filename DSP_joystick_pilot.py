#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.82.01), Mi 20 Mai 15:16:34 2015
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
import matplotlib as mlib
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
from random import randint # random function for random sequence production
from psychopy.contrib import mseq
import csv
import cPickle as pickle
#import serial
import time
import itertools

GAIN=14


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'DSP_8target_day1'  # from the Builder filename that created this script
expInfo = {'participant':'', 'session':'001', 'Flip X':False}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

# Define target coordinates, from left clock-wise
targets=[(-0.8,0), (-0.5657,-0.5657), (0,-0.8), (0.5657,-0.5657), (0.8,0), (0.5657,0.5657), (0,0.8), (-0.5657,0.5657)]
target_times=[] # times when targets were reached
targets_reached=0
target_number=[] #definiert den targetindex (siehe targets) fürs zufallstarget
target_timecourse=[] # time series of targets
trial_success=[] # list indicating whether trials were successfull
joy_x=[]
joy_y=[]
trialNum=0 # current trial-index
seq_id=[] # identifier of sequence type
seq_num=[] # identifies the number of the ongoing sequnece for each frame
sequence_length=8 # must be 8!rial!! set sequence length

flipped_sequence = np.array([
                     4,3,2,1,0,7,6,5],dtype=np.int)

def get_targets(sequence):
    if not expInfo["Flip X"]:
        return sequence
    return flipped_sequence[np.array(sequence)]

# Define sequences in target order: random: seq_id=0; Sequence A: seq-id=1; Sequence B: seq_id=2
target_order=['random',get_targets((0,2,5,3,1,4,5,6)),get_targets((6,7,4,1,0,3,7,5))]
seq_label=['random', 'A', 'B']

# create list of 50 random trials followed by 250 item m-sequence representing 2 trial types (A(1), B(2))
#trialorderlist=(np.append(np.zeros(50), (mseq.mseq(2,8,4,1)[:250]+1))).tolist()
#trialorderlist=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
trialorderlist=list(itertools.chain(np.zeros(20), (mseq.mseq(2,6,10,1)[:40]+1).tolist()))
trialorderlist=[1,2,1,2,1,2,1,2]

# create .csv output file
csvfile = open('trialorder_day1_sub_'+expInfo['participant']+'.csv', 'wb')
writer = csv.writer(csvfile)
writer.writerows([trialorderlist])
csvfile.close()

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file
endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(size=(1280, 800), fullscr=True, screen=1, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    )
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# Initialize components for Routine "instruction"
instructionClock = core.Clock()
text_instruction = visual.TextStim(win=win, ori=0, name='text_instruction',
    text='Move to indicated target and back to the center as fast as possbile',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "routine_8targets_trial"
routine_8targets_trialClock = core.Clock()
# setup serial port
#ser = serial.Serial('/dev/ttyACM0',9600)
#ser = serial.Serial('/dev/ttyUSB0',9600)
from arduino_comm import ArduinoComm
ser = ArduinoComm("COM5")

text_reward_trial_cue_seq = visual.TextStim(win=win, ori=0, name='text_reward_trail_cue_seq',
    text='default text',    font='Arial',
    pos=[0, 0.3], height=0.2, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)
joy_circle = visual.Polygon(win=win, name='joy_circle',
    edges = 90, size=[0.02, 0.02],
    ori=0, pos=[0, 0],
    lineWidth=1, lineColor='black', lineColorSpace='rgb',
    fillColor='red', fillColorSpace='rgb',
    opacity=1,depth=-10.0, 
interpolate=True)
circle = visual.Polygon(win=win, name='circle',
    edges = 90, size=[0.2, 0.2],
    ori=0, pos=[0, 0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1,depth=-1.0, 
interpolate=True)
circle_up_cen = visual.Polygon(win=win, name='circle_up_cen',
    edges = 90, size=[0.2, 0.2],
    ori=0, pos=[0, -0.8],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1,depth=-1.0, 
interpolate=True)
circle_down_cen = visual.Polygon(win=win, name='circle_down_cen',
    edges = 90, size=[0.2, 0.2],
    ori=0, pos=[0, 0.8],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1,depth=-2.0, 
interpolate=True)
circle_left = visual.Polygon(win=win, name='circle_left',
    edges = 90, size=[0.2, 0.2],
    ori=0, pos=[-0.8, 0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1,depth=-3.0, 
interpolate=True)
circle_right = visual.Polygon(win=win, name='circle_right',
    edges = 90, size=[0.2, 0.2],
    ori=0, pos=[0.8, 0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1,depth=-4.0, 
interpolate=True)
circle_up_ri = visual.Polygon(win=win, name='circle_up_ri',
    edges = 90, size=[0.2, 0.2],
    ori=0, pos=[0.5657, 0.5657],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1,depth=-5.0, 
interpolate=True)
circle_down_ri = visual.Polygon(win=win, name='circle_down_ri',
    edges = 90, size=[0.2, 0.2],
    ori=0, pos=[0.5657, -0.5657],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1,depth=-6.0, 
interpolate=True)
circle_up_left = visual.Polygon(win=win, name='circle_up_left',
    edges = 90, size=[0.2, 0.2],
    ori=0, pos=[-0.5657, 0.5657],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1,depth=-7.0, 
interpolate=True)
circle_down_left = visual.Polygon(win=win, name='circle_down_left',
    edges = 90, size=[0.2, 0.2],
    ori=0, pos=[-0.5657, -0.5657],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1,depth=-8.0, 
interpolate=True)
target_circle = visual.Polygon(win=win, name='circle',
    edges = 90, size=[0.2, 0.2],
    ori=0, pos=[0, 0],
    lineWidth=1, lineColor='red', lineColorSpace='rgb',
    fillColor='red', fillColorSpace='rgb',
    opacity=1,depth=-9.0, 
interpolate=True)
x, y = [None, None]
joy_x = []
joy_y = []
joy_time = []


    


# Initialize components for Routine "end"
endClock = core.Clock()
text_end = visual.TextStim(win=win, ori=0, name='text',
    text='Thanks for participating',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)
    
#Re-installize variables if screen needs to be flipped
if expInfo['Flip X'] == (True):
    text_instruction = visual.TextStim(win=win, ori=0, name='text_instruction',
        text='Move to indicated target and back to the center as fast as possbile',    font='Arial',
        pos=[0, 0], height=0.1, wrapWidth=None,
        color='white', colorSpace='rgb',flipHoriz=True, opacity=1,
        depth=0.0)
    text_reward_trial_cue_seq = visual.TextStim(win=win, ori=0, name='text_reward_trail_cue_seq',
        text='default text',    font='Arial',
        pos=[0, 0.3], height=0.2, wrapWidth=None,
        color='white', colorSpace='rgb',flipHoriz=True, opacity=1,
        depth=0.0)
    text_end = visual.TextStim(win=win, ori=0, name='text',
        text='Thanks for participating',    font='Arial',
        pos=[0, 0], height=0.1, wrapWidth=None,
        color='white', colorSpace='rgb', flipHoriz=True, opacity=1,
        depth=0.0)
    

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

#------Prepare to start Routine "instruction"-------
t = 0
instructionClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
key_resp_instruct = event.BuilderKeyResponse()  # create an object of type KeyResponse
key_resp_instruct.status = NOT_STARTED
# keep track of which components have finished
instructionComponents = []
instructionComponents.append(text_instruction)
instructionComponents.append(key_resp_instruct)
for thisComponent in instructionComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "instruction"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = instructionClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_instruction* updates
    if t >= 0.0 and text_instruction.status == NOT_STARTED:
        # keep track of start time/frame for later
        text_instruction.tStart = t  # underestimates by a little under one frame
        text_instruction.frameNStart = frameN  # exact frame index
        text_instruction.setAutoDraw(True)
    
    # *key_resp_instruct* updates
    if t >= 0.0 and key_resp_instruct.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_instruct.tStart = t  # underestimates by a little under one frame
        key_resp_instruct.frameNStart = frameN  # exact frame index
        key_resp_instruct.status = STARTED
        # keyboard checking is just starting
        key_resp_instruct.clock.reset()  # now t=0
        event.clearEvents(eventType='keyboard')
    if key_resp_instruct.status == STARTED:
        theseKeys = event.getKeys()
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_instruct.keys = theseKeys[-1]  # just the last key pressed
            key_resp_instruct.rt = key_resp_instruct.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instructionComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "instruction"-------
for thisComponent in instructionComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_instruct.keys in ['', [], None]:  # No response was made
   key_resp_instruct.keys=None
# store data for thisExp (ExperimentHandler)
thisExp.addData('key_resp_instruct.keys',key_resp_instruct.keys)
if key_resp_instruct.keys != None:  # we had a response
    thisExp.addData('key_resp_instruct.rt', key_resp_instruct.rt)
thisExp.nextEntry()
# the Routine "instruction" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=len(trialorderlist), method='random', 
    extraInfo=expInfo, originPath=None,
    trialList=[None],
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial.keys():
        exec(paramName + '= thisTrial.' + paramName)
        
for thisTrial in trials:
    currentLoop = trials
    # Determine upcomming sequence (random for now)
    seq_id.append(int(trialorderlist[trialNum]))
    
    # insert a break after each 50 trials (using the instruction routine)
    if len(seq_id)>2 and ((len(seq_id))-1)%50==0:
        #------Prepare to start Routine "instruction"-------
        t = 0
        instructionClock.reset()  # clock 
        frameN = -1
        # update component parameters for each repeat
        key_resp_instruct = event.BuilderKeyResponse()  # create an object of type KeyResponse
        key_resp_instruct.status = NOT_STARTED
        # keep track of which components have finished
        instructionComponents = []
        instructionComponents.append(text_instruction)
        instructionComponents.append(key_resp_instruct)
        text_instruction.setText("Have a break and continue with ENTER")
        for thisComponent in instructionComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "instruction"-------
        continueRoutine = True
        while continueRoutine:
            # get current time
            t = instructionClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *text_instruction* updates
            if t >= 0.0 and text_instruction.status == NOT_STARTED:
                # keep track of start time/frame for later
                text_instruction.tStart = t  # underestimates by a little under one frame
                text_instruction.frameNStart = frameN  # exact frame index
                text_instruction.setAutoDraw(True)
            
            # *key_resp_instruct* updates
            if t >= 0.0 and key_resp_instruct.status == NOT_STARTED:
                # keep track of start time/frame for later
                key_resp_instruct.tStart = t  # underestimates by a little under one frame
                key_resp_instruct.frameNStart = frameN  # exact frame index
                key_resp_instruct.status = STARTED
                # keyboard checking is just starting
                key_resp_instruct.clock.reset()  # now t=0
                event.clearEvents(eventType='keyboard')
            if key_resp_instruct.status == STARTED:
                theseKeys = event.getKeys()
                
                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    key_resp_instruct.keys = theseKeys[-1]  # just the last key pressed
                    key_resp_instruct.rt = key_resp_instruct.clock.getTime()
                    # a response ends the routine
                    continueRoutine = False
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in instructionComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "instruction"-------
        for thisComponent in instructionComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if key_resp_instruct.keys in ['', [], None]:  # No response was made
           key_resp_instruct.keys=None
        # store data for thisExp (ExperimentHandler)
        thisExp.addData('key_resp_instruct.keys',key_resp_instruct.keys)
        if key_resp_instruct.keys != None:  # we had a response
            thisExp.addData('key_resp_instruct.rt', key_resp_instruct.rt)
        thisExp.nextEntry()
        # the Routine "instruction" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)
            
    #------Prepare to start Routine "routine_8targets_trial"-------
    t = 0
    targets_reached=0 # re-sets number of already reached targets (targets_reached==8 sequence will terminate)
    target_status=0 # always start with center target
    routine_8targets_trialClock.reset()  # clock 
    frameN = -1
    # update sequnece information for upcomming trial
    text_reward_trial_cue_seq.setText('Sequence: %s' %(seq_label[seq_id[-1]])) #S et text of sequence cue ("trial cue") to following sequence (seq_id)
    
    # keep track of which components have finished
    routine_8targets_trialComponents = []
    routine_8targets_trialComponents.append(text_reward_trial_cue_seq)
    routine_8targets_trialComponents.append(joy_circle)
    routine_8targets_trialComponents.append(circle)
    routine_8targets_trialComponents.append(circle_up_cen)
    routine_8targets_trialComponents.append(circle_down_cen)
    routine_8targets_trialComponents.append(circle_left)
    routine_8targets_trialComponents.append(circle_right)
    routine_8targets_trialComponents.append(circle_up_ri)
    routine_8targets_trialComponents.append(circle_down_ri)
    routine_8targets_trialComponents.append(circle_up_left)
    routine_8targets_trialComponents.append(circle_down_left)
    routine_8targets_trialComponents.append(target_circle)
    for thisComponent in routine_8targets_trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "routine_8targets_trial"-------
    # send record initiating ASCII code to SD arduino
    #ser.trial_begin()
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = routine_8targets_trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        #while True:
            #try:
        x,y = ser.measure()
                #break
            #except Exception,e:
                #pass
        if expInfo['Flip X'] == (True):
            joy_x.append((-(x-511.5)/511.5)*GAIN)
            joy_y.append(((y-511.5)/511.5)*GAIN)
            joy_circle.pos = [joy_x[-1], joy_y[-1]]
            target_timecourse.append(target_status)
            seq_num.append(trialNum)
        if expInfo['Flip X'] == (False):
            joy_x.append(((x-511.5)/511.5)*GAIN)
            joy_y.append(((y-511.5)/511.5)*GAIN)
            joy_circle.pos = [joy_x[-1], joy_y[-1]]
            target_timecourse.append(target_status)
            seq_num.append(trialNum)
        
        # update/draw components on each frame
        # *text_trial_cue_seq* updates
        if t >= 0.0 and text_reward_trial_cue_seq.status == NOT_STARTED:
            # keep track of start time/frame for later
            text_reward_trial_cue_seq.tStart = t  # underestimates by a little under one frame
            text_reward_trial_cue_seq.frameNStart = frameN  # exact frame index
            text_reward_trial_cue_seq.setAutoDraw(True)
        if text_reward_trial_cue_seq.status == STARTED and t >= 2.0: #most of one frame period left
            text_reward_trial_cue_seq.setAutoDraw(False)
        
        # *circle* updates
        if t >= 2.0 and circle.status == NOT_STARTED:
            # keep track of start time/frame for later
            circle.tStart = t  # underestimates by a little under one frame
            circle.frameNStart = frameN  # exact frame index
            circle.setAutoDraw(True)
        
        # *circle_up_cen* updates
        if t >= 2.0 and circle_up_cen.status == NOT_STARTED:
            # keep track of start time/frame for later
            circle_up_cen.tStart = t  # underestimates by a little under one frame
            circle_up_cen.frameNStart = frameN  # exact frame index
            circle_up_cen.setAutoDraw(True)
        
        # *circle_down_cen* updates
        if t >= 2.0 and circle_down_cen.status == NOT_STARTED:
            # keep track of start time/frame for later
            circle_down_cen.tStart = t  # underestimates by a little under one frame
            circle_down_cen.frameNStart = frameN  # exact frame index
            circle_down_cen.setAutoDraw(True)
        
        # *circle_left* updates
        if t >= 2.0 and circle_left.status == NOT_STARTED:
            # keep track of start time/frame for later
            circle_left.tStart = t  # underestimates by a little under one frame
            circle_left.frameNStart = frameN  # exact frame index
            circle_left.setAutoDraw(True)
        
        # *circle_right* updates
        if t >= 2.0 and circle_right.status == NOT_STARTED:
            # keep track of start time/frame for later
            circle_right.tStart = t  # underestimates by a little under one frame
            circle_right.frameNStart = frameN  # exact frame index
            circle_right.setAutoDraw(True)
        
        # *circle_up_ri* updates
        if t >= 2.0 and circle_up_ri.status == NOT_STARTED:
            # keep track of start time/frame for later
            circle_up_ri.tStart = t  # underestimates by a little under one frame
            circle_up_ri.frameNStart = frameN  # exact frame index
            circle_up_ri.setAutoDraw(True)
        
        # *circle_down_ri* updates
        if t >= 2.0 and circle_down_ri.status == NOT_STARTED:
            # keep track of start time/frame for later
            circle_down_ri.tStart = t  # underestimates by a little under one frame
            circle_down_ri.frameNStart = frameN  # exact frame index
            circle_down_ri.setAutoDraw(True)
        
        # *circle_up_left* updates
        if t >= 2.0 and circle_up_left.status == NOT_STARTED:
            # keep track of start time/frame for later
            circle_up_left.tStart = t  # underestimates by a little under one frame
            circle_up_left.frameNStart = frameN  # exact frame index
            circle_up_left.setAutoDraw(True)
        
        # *circle_down_left* updates
        if t >= 2.0 and circle_down_left.status == NOT_STARTED:
            # keep track of start time/frame for later
            circle_down_left.tStart = t  # underestimates by a little under one frame
            circle_down_left.frameNStart = frameN  # exact frame index
            circle_down_left.setAutoDraw(True)
            
        # *joy_circle* updates
        if t >= 2.0 and joy_circle.status == NOT_STARTED:
            # keep track of start time/frame for later
            # send record initiating ASCII code to SD arduino
            ser.trial_begin()
            joy_circle.tStart = t  # underestimates by a little under one frame
            joy_circle.frameNStart = frameN  # exact frame index
            joy_circle.status = STARTED
        if t >= 2.0 and joy_circle.status == STARTED:  # only update if started and not stopped!
            joy_circle.setAutoDraw(True)
            
            # Taget Bedingungen center=0 oder outside=1
            if t >= 2.0 and (target_status==0):
               # Draw target cirlce in middle
               target_circle.pos=[0,0]
               target_circle.tStart = t  # underestimates by a little under one frame
               target_circle.frameNStart = frameN
               target_circle.setAutoDraw(True)
               
               if ( (joy_x[-1]<=0.1) and (joy_x[-1]>=-0.1) and (joy_y[-1]>=-0.1) and (joy_y[-1]<=0.1)):
               # query whether random or learning sequence should be produced
                if targets_reached==sequence_length:   # if 8 outside targets are reached and middle circle is touched again
                    trial_success.append(1)
                    continueRoutine=False
                elif seq_id[-1]==0:
                    # create next outside target randomly
                    target_number.append(randint(0,7)) # target number=target index, see targets
                    target_circle.pos=targets[(target_number[-1])]
                    #target_times.append(t)
                elif seq_id[-1]!=0:
                    # use predetermined target_order
                    target_number.append(target_order[seq_id[-1]][targets_reached]) # target number=target index, see targets
                    target_circle.pos=targets[(target_number[-1])]
                # Draw target cirlce
                target_circle.tStart = t  # underestimates by a little under one frame
                target_circle.frameNStart = frameN
                target_circle.setAutoDraw(True)
                target_times.append(globalClock.getTime())
                target_status=1
                ser.trial_trajectory_away()
                
            elif t >= 2.0 and (target_status==1):
               if ( (joy_x[-1]<=((targets[(target_number[-1])][0])+0.1) and (joy_x[-1]>=((targets[(target_number[-1])][0])-0.1) 
               and (joy_y[-1]>=((targets[(target_number[-1])][1])-0.1)) and (joy_y[-1]<=((targets[(target_number[-1])][1])+0.1))))):
                target_circle.pos=[0,0]
                # Draw target cirlce in middle
                target_circle.tStart = t  # underestimates by a little under one frame
                target_circle.frameNStart = frameN
                target_circle.setAutoDraw(True)
                targets_reached+=1
                target_times.append(globalClock.getTime())
                target_status=0
                ser.trial_trajectory_center()
                
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in routine_8targets_trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "routine_8targets_trial"-------
    for thisComponent in routine_8targets_trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # send record initiating ASCII code to SD arduino
    ser.trial_end()
    # store data for trials (TrialHandler)
    trials.addData('joy_x', joy_x)
    trials.addData('joy_y', joy_y)
    #trials.addData('mouse.time', mouse.time)
    # the Routine "routine_8targets_trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    trialNum+=1
    thisExp.nextEntry()
    

    
# completed 5 repeats of 'trials'

# experimental data
savename = ('data/Day1_' + expInfo['participant'] + '_' + expInfo['date'])
expData=[joy_x,joy_y,target_timecourse,seq_num,seq_id]
np.save(savename+'_expData', expData) # to load expData=np.load('expData.npy') after import numpy as np
np.save(savename+'_target_times', target_times) # to load target_times=np.load('target_times.npy') after import numpy as np


#------Prepare to start Routine "end"-------
t = 0
endClock.reset()  # clock 
frameN = -1
routineTimer.add(2.000000)
# update component parameters for each repeat
# keep track of which components have finished
endComponents = []
endComponents.append(text_end)
for thisComponent in endComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "end"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = endClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_end* updates
    if t >= 0.0 and text_end.status == NOT_STARTED:
        # keep track of start time/frame for later
        text_end.tStart = t  # underestimates by a little under one frame
        text_end.frameNStart = frameN  # exact frame index
        text_end.setAutoDraw(True)
    if text_end.status == STARTED and t >= (0.0 + (2.0-win.monitorFramePeriod*0.75)): #most of one frame period left
        text_end.setAutoDraw(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "end"-------
for thisComponent in endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
#ser.close()
win.close()
core.quit()
