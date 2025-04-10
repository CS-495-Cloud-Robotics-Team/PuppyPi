# Payload Dictionary with JSON payloads

payloads_dict = {
    "two-legs-stand": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "2_legs_stand.d6ac",
            "wait": True
        }
    },
    "bow": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "bow.d6ac",
            "wait": True
        }
    },
    "boxing-main": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "boxing.d6ac",
            "wait": True
        }
    },
    "boxing-alt": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "boxing2.d6ac",
            "wait": True
        }
    },
    "grab": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "grab.d6a",
            "wait": True
        }
    },
    "jump": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "jump.d6ac",
            "wait": True
        }
    },
    "kick-ball-left": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "kick_ball_left.d6ac",
            "wait": True
        }
    },
    "kick-ball-left-bak": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "kick_ball_left_bak.d6ac",
            "wait": True
        }
    },
    "kick-ball-right": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "kick_ball_right.d6ac",
            "wait": True
        }
    },
    "lie-down": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "lie_down.d6ac",
            "wait": True
        }
    },
    "look-down-short": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "look_down.d6a",
            "wait": True
        }
    },
    "look-down": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "look_down.d6ac",
            "wait": True
        }
    },
    "moonwalk": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "moonwalk.d6ac",
            "wait": True
        }
    },
    "nod": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "nod.d6ac",
            "wait": True
        }
    },
    "pee": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "pee.d6ac",
            "wait": True
        }
    },
    "place-main": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "place.d6a",
            "wait": True
        }
    },
    "place-alt": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "place1.d6a",
            "wait": True
        }
    },
    "push-up": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "push-up.d6ac",
            "wait": True
        }
    },
    "run": [
        {
        "op": "call_service",
            "service": "/puppy_control/set_running",
            "args": {
                "data": True
            }
        },
        {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "stand.d6ac",
            "wait": True
        }
        },
        {
            "wait": 0.2
        },
        {
        "op": "publish",
            "topic": "/cmd_vel",
            "msg": {
                "linear": {"x": 2.0, "y": 0.0, "z": 0.0},
                "angular": {"x": 0.0, "y": 0.0, "z": 0.0}
            }
        },
        {
            "wait": 2.5
        },
        {
        "op": "publish",
            "topic": "/cmd_vel",
            "msg": {
                "linear": {"x": 0.0, "y": 0.0, "z": 0.0},
                "angular": {"x": 0.0, "y": 0.0, "z": 0.0}
            }
        }
    ],
    "shake-hands": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "shake_hands.d6ac",
            "wait": True
        }
    },
    "shake-head": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "shake_head.d6ac",
            "wait": True
        }
    },
    "sit": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "sit.d6ac",
            "wait": True
        }
    },
    "spacewalk": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "spacewalk.d6ac",
            "wait": True
        }
    },
    "stand-short": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "stand.d6a",
            "wait": True
        }
    },
    "stand": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "stand.d6ac",
            "wait": True
        }
    },
    "stand-with-arm": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "stand_with_arm.d6a",
            "wait": True
        }
    },
    "stop": {
        "op": "publish",
            "topic": "/cmd_vel",
            "msg": {
                "linear": {"x": 0.0, "y": 0.0, "z": 0.0},
                "angular": {"x": 0.0, "y": 0.0, "z": 0.0}
            }
    },
    "stretch": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "stretch.d6ac",
            "wait": True
        }
    },
    "temp": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "temp.d6ac",
            "wait": True
        }
    },
    "turn-around": [
        {
        "op": "call_service",
            "service": "/puppy_control/set_running",
            "args": {
                "data": True
            }
        },
        {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "stand.d6ac",
            "wait": True
        }
        },
        {
            "wait": 0.2
        },
        {
        "op": "publish",
            "topic": "/cmd_vel",
            "msg": {
                "linear": {"x": 0.0, "y": 0.0, "z": 0.0},
                "angular": {"x": 0.0, "y": 0.0, "z": 1.5}
            }
        },
        {
            "wait": 4.06
        },
        {
        "op": "publish",
            "topic": "/cmd_vel",
            "msg": {
                "linear": {"x": 0.0, "y": 0.0, "z": 0.0},
                "angular": {"x": 0.0, "y": 0.0, "z": 0.0}
            }
        }
    ],
    "turn-left": [
        {
        "op": "call_service",
            "service": "/puppy_control/set_running",
            "args": {
                "data": True
            }
        },
        {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "stand.d6ac",
            "wait": True
        }
        },
        {
            "wait": 0.2
        },
        {
        "op": "publish",
            "topic": "/cmd_vel",
            "msg": {
                "linear": {"x": 0.0, "y": 0.0, "z": 0.0},
                "angular": {"x": 0.0, "y": 0.0, "z": 1.5}
            }
        },
        {
            "wait": 2.03
        },
        {
        "op": "publish",
            "topic": "/cmd_vel",
            "msg": {
                "linear": {"x": 0.0, "y": 0.0, "z": 0.0},
                "angular": {"x": 0.0, "y": 0.0, "z": 0.0}
            }
        },
    ],
    "turn-right": [
        {
        "op": "call_service",
            "service": "/puppy_control/set_running",
            "args": {
                "data": True
            }
        },
        {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "stand.d6ac",
            "wait": True
        }
        },
        {
            "wait": 0.2
        },
        {
        "op": "publish",
            "topic": "/cmd_vel",
            "msg": {
                "linear": {"x": 0.0, "y": 0.0, "z": 0.0},
                "angular": {"x": 0.0, "y": 0.0, "z": -1.5}
            }
        },
        {
            "wait": 2.03
        },
        {
        "op": "publish",
            "topic": "/cmd_vel",
            "msg": {
                "linear": {"x": 0.0, "y": 0.0, "z": 0.0},
                "angular": {"x": 0.0, "y": 0.0, "z": 0.0}
            }
        },
    ],
    "up-stairs-2cm": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "up_stairs_2cm.d6ac",
            "wait": True
        }
    },
    "up-stairs-3.5cm": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "up_stairs_3.5cm.d6ac",
            "wait": True
        }
    },
    "up-stairs-3.5cm-alt0": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "up_stairs_3.5cm0.d6ac",
            "wait": True
        }
    },
    "up-stairs-3.5cm-alt1": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "up_stairs_3.5cm1.d6ac",
            "wait": True
        }
    },
    "wave": {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "wave.d6ac",
            "wait": True
        }
    },
    "walk": [
        {
        "op": "call_service",
            "service": "/puppy_control/set_running",
            "args": {
                "data": True
            }
        },
        {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "stand.d6ac",
            "wait": True
        }
        },
        {
            "wait": 0.2
        },
        {
        "op": "publish",
            "topic": "/cmd_vel",
            "msg": {
                "linear": {"x": 1.0, "y": 0.0, "z": 0.0},
                "angular": {"x": 0.0, "y": 0.0, "z": 0.0}
            }
        },
        {
            "wait": "{{walk_time}}"
        },
        {
        "op": "publish",
            "topic": "/cmd_vel",
            "msg": {
                "linear": {"x": 0.0, "y": 0.0, "z": 0.0},
                "angular": {"x": 0.0, "y": 0.0, "z": 0.0}
            }
        }
    ],
    "walk-backward": [
        {
        "op": "call_service",
            "service": "/puppy_control/set_running",
            "args": {
                "data": True
            }
        },
        {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "stand.d6ac",
            "wait": True
        }
        },
        {
            "wait": 0.2
        },
        {
        "op": "publish",
            "topic": "/cmd_vel",
            "msg": {
                "linear": {"x": -1.0, "y": 0.0, "z": 0.0},
                "angular": {"x": 0.0, "y": 0.0, "z": 0.0}
            }
        },
        {
            "wait": 2.5
        },
        {
        "op": "publish",
            "topic": "/cmd_vel",
            "msg": {
                "linear": {"x": 0.0, "y": 0.0, "z": 0.0},
                "angular": {"x": 0.0, "y": 0.0, "z": 0.0}
            }
        }
        
    ],

    "dance_routine": [
        {
            "op": "call_service",
            "service": "/puppy_control/runActionGroup",
            "args": {
                "name": "stand.d6ac",
                "wait": True
            }
        },
        {
            "op": "call_service",
            "service": "/puppy_control/runActionGroup",
            "args": {
                "name": "moonwalk.d6ac",
                "wait": True
            }
        },
        {
            "op": "call_service",
            "service": "/puppy_control/runActionGroup",
            "args": {
                "name": "wave.d6ac",
                "wait": True
            }
        }
    ]     
}
