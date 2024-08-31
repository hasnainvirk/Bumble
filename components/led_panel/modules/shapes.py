"""
This module contains the shapes that can be displayed on the LED panel.
"""

bob_eyes_open = (
    0x10,
    0x28,
    0x54,
    0x54,
    0x54,
    0x28,
    0x12,
    0x01,
    0x01,
    0x12,
    0x28,
    0x54,
    0x54,
    0x54,
    0x28,
    0x10,
)

bob_eyes_dead = (
    0x00,
    0x00,
    0x00,
    0x10,
    0x10,
    0x10,
    0x02,
    0x01,
    0x01,
    0x02,
    0x10,
    0x10,
    0x10,
    0x00,
    0x00,
    0x00,
)

bob_eyes_shut = (
    0x10,
    0x28,
    0x44,
    0x44,
    0x44,
    0x28,
    0x12,
    0x01,
    0x01,
    0x12,
    0x28,
    0x44,
    0x44,
    0x44,
    0x28,
    0x10,
)


smile = (
    0x00,
    0x00,
    0x38,
    0x40,
    0x40,
    0x40,
    0x3A,
    0x02,
    0x02,
    0x3A,
    0x40,
    0x40,
    0x40,
    0x38,
    0x00,
    0x00,
)
matrix_forward = (
    0x00,
    0x00,
    0x00,
    0x00,
    0x12,
    0x24,
    0x48,
    0x90,
    0x90,
    0x48,
    0x24,
    0x12,
    0x00,
    0x00,
    0x00,
    0x00,
)
matrix_back = (
    0x00,
    0x00,
    0x00,
    0x00,
    0x48,
    0x24,
    0x12,
    0x09,
    0x09,
    0x12,
    0x24,
    0x48,
    0x00,
    0x00,
    0x00,
    0x00,
)
matrix_left = (
    0x00,
    0x00,
    0x00,
    0x00,
    0x18,
    0x24,
    0x42,
    0x99,
    0x24,
    0x42,
    0x81,
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
)
matrix_right = (
    0x00,
    0x00,
    0x00,
    0x00,
    0x00,
    0x81,
    0x42,
    0x24,
    0x99,
    0x42,
    0x24,
    0x18,
    0x00,
    0x00,
    0x00,
    0x00,
)
