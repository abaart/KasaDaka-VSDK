# ForobaBlon-SPS
This repository holds the Foroba Blon prototype project which was part of the project assignment of a seven week Master course called "ICT4D: Information and Communication Technology for Development" at the Vrije Universiteit (https://www.vu.nl/).

Foroba Blon is part of W4RA (https://w4ra.org/w4ra/), which tries to use computer science to help rural sustainable development. Foroba Blon tries to help rural communities to allow citizen journalism, with a voice-based/phone-based service to call to the radio station (https://w4ra.org/foroba-blon-community-radio-in-africa-and-the-web/) and allow people to vote, or leave voice messages. The project uses Kasdaka to accomplish this, more information about Kasadaka can be found in the section called Kasadaka.

## Context
The project takes is mode for people in rural areas. In these areas literacy is not always high, and digital literacy can even be lower. There for the solution is made in such a way that it would fit these need.

# Participants
The GitHub names of the participants are:
- FunkeMT 
- wkokgit
- mrthefastfender
- pjotrscholtze

# Kasadaka
Kasadaka is a Django based solution for managing voice based services. Kasadaka is specifically made for ICT4D, and generates VXML documents that contain the voice menus, references and links back to Kasadaka to generate new and dynamic documents. We extended the Kasadaka platform for our project with new features. The project is forked from th original Kasadaka repository: https://github.com/abaart/KasaDaka-VSDK

# How does it work
The project allows two actors to operate with the platform, the radio host and the listener. The radio host sets up a question, and the callers can call to our platform. The system will anwser the call and the the caller can vote with the keypad of their phone and/or leave a message. The radio host can see the results on a webpage and playback certain calls.

## Example video
@todo


# License
The MIT License (MIT)

Copyright (c) 2020 Markus Funke, Sven Preng, Wouter Kok, Pjotr Scholtze

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.




