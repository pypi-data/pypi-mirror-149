# ihypy
WIP Python musical analysis module

# Install
`py -m pip install ihypy` for Windows
`python3 -m pip install ihypy` otherwise

# Description
Where does the name come from? I wanted something musical that rhymed with py, and Ihy apparently is an Egyptian god of music—more specifically, the ectasy of playing the sistrum. Whether or not that actually rhymes, I am pronouncing the name of this repository as "I Hi Py" as it looks like it should rhyme, and the sistrum's heiroglyph looks cool. 𓏣

# Purpose
More than anything else, I want to familiarize myself with how to do stuff on Github but keeping it interesting by doing musicology stuff. I want to create a framework that allows for the creation of many different ethnic music background to be explored, while providing just some basic Western classical instances.

# Framework
I will be trying to use abc.ABC for abstraction and docstring/type annotations. I am honestly still not really used to doing this in Python, but I want to try at least, even if the docstrings are poorly written for now.

There will only be a few base/abstract classes that really lay out the groundwork as I get started: Note, NotationError, TuningSystem, NotationSystem, and MusicalSystem. MusicalSystem itself is really built out of the combination of a TuningSystem and NotationSystem, and everything else will be derivative from that.

I have not come up with any functional interfaces yet, though they might come if necessary. At the moment, I have not thought of such an example unless I introduce different units of measure in music (e.g. Hz vs. cent or comparing enharmonic pitches), but at the moment, I do not want to tie my hands up in that mess.

# Systems
My goal is to first create a couple of simple types of systems. 

Tuning
- 12 TET
- Just intonation
- Pythagorean intonation

Notation
- IPN
- Helmholtz pitch notation

Musical
- Western classical

# Audio and Transcription
There will likely be some audio based stuff too. If I can create a note, it would be nice to hear it. I could turn this into pseudo musical notation if I can define something like a Piece class that describes when and what notes should be played. If nothing else, it would be nice to be able to break down chords. 

If possible, I would also like to be able to transcribe from any of the following sources for analysis:
- Sheet music
- MIDI
- Audio (i.e. actual recordings)

I do not ever plan to create something that write sheet music.

# Testing
I will also attempt to run tests. I will undoubtedly miss many things, but that is ok. I just want to learn how to write tests and improve at it. I will test stuff along the way, but I will run larger scale tests as well.

# Time Frame
In terms of scheduling and timing, I am in no rush. This is a project I am doing for fun, so updates will likely not be regular. However, I hope that I will not stall the project for a long time.

It would be nice to have at least some of audio/transcription stuff along with tuning, notation, and musical systems done in a month-ish, but who knows? If I get that, I might be able to make a first release of a module, but we shall see.