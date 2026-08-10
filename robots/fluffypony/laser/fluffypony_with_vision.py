#!/usr/bin/env python3
import sys
sys.path.insert(0, '/tmp/I-ECO-01/robots/shared/vision')
from smart_camera import FluffyponyVision

vision = FluffyponyVision()
vision.check_glass()
vision.detect_person()
