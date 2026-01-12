import math
import numpy as np
import torch
from PIL import Image, ImageDraw


class CameraAnglePromptBuilder:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "subject_token": (
                    "STRING",
                    {
                        "default": "<sks>",
                        "multiline": False,
                    },
                ),
                "orbit": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 7,
                        "step": 1,
                        "display": "slider",
                    },
                ),
                "pitch": (
                    "INT",
                    {
                        "default": 1,
                        "min": 0,
                        "max": 3,
                        "step": 1,
                        "display": "slider",
                    },
                ),
                "zoom": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 2,
                        "step": 1,
                        "display": "slider",
                    },
                ),
            }
        }

    RETURN_TYPES = ("STRING", "IMAGE")
    RETURN_NAMES = ("prompt", "camera_diagram")
    FUNCTION = "build_prompt"
    CATEGORY = "Prompt / Camera"

    ORBIT_OPTIONS = [
        "front",
        "front-right quarter",
        "right side",
        "back-right quarter",
        "back",
        "back-left quarter",
        "left side",
        "front-left quarter",
    ]

    PITCH_OPTIONS = [
        "low-angle shot",
        "eye-level shot",
        "elevated shot",
        "high-angle shot",
    ]

    ZOOM_OPTIONS = [
        "close-up",
        "medium shot",
        "wide shot",
    ]

    def build_prompt(self, subject_token, orbit, pitch, zoom):
        orbit = max(0, min(orbit, len(self.ORBIT_OPTIONS) - 1))
        pitch = max(0, min(pitch, len(self.PITCH_OPTIONS) - 1))
        zoom = max(0, min(zoom, len(self.ZOOM_OPTIONS) - 1))

        parts = []
        if subject_token.strip():
            parts.append(subject_token.strip())

        parts.append(f"{self.ORBIT_OPTIONS[orbit]} view")
        parts.append(self.PITCH_OPTIONS[pitch])
        parts.append(self.ZOOM_OPTIONS[zoom])

        prompt = " ".join(parts)

        diagram_pil = self._draw_camera_diagram(orbit, pitch, zoom)
        diagram_image = self._pil_to_comfy_image(diagram_pil)

        return (prompt, diagram_image)

    def _draw_camera_diagram(self, orbit, pitch, zoom):
        width = 512
        height = 256
        img = Image.new("RGB", (width, height), (30, 30, 30))
        draw = ImageDraw.Draw(img)

        left_center_x = 128
        right_center_x = 384
        center_y = height // 2

        ground_y = center_y + 50
        draw.line([20, ground_y, 236, ground_y], fill=(90, 90, 90), width=2)

        subject_radius_map = {0: 16, 1: 12, 2: 8}
        subject_r = subject_radius_map[zoom]

        subject_x = left_center_x
        subject_y = ground_y - subject_r

        draw.ellipse(
            [
                subject_x - subject_r,
                subject_y - subject_r * 2,
                subject_x + subject_r,
                subject_y,
            ],
            fill=(220, 220, 220),
        )

        camera_height_map = {
            0: ground_y + 30,
            1: subject_y - subject_r,
            2: subject_y - 40,
            3: subject_y - 80,
        }

        cam_x = left_center_x - 70
        cam_y = camera_height_map[pitch]

        draw.line(
            [cam_x, ground_y + 40, cam_x, ground_y - 100],
            fill=(80, 80, 80),
            width=2,
        )

        draw.ellipse(
            [cam_x - 6, cam_y - 6, cam_x + 6, cam_y + 6],
            fill=(100, 180, 255),
        )

        draw.line(
            [cam_x + 6, cam_y, subject_x - subject_r, subject_y - subject_r],
            fill=(100, 180, 255),
            width=2,
        )

        orbit_radius = 70
        draw.ellipse(
            [
                right_center_x - orbit_radius,
                center_y - orbit_radius,
                right_center_x + orbit_radius,
                center_y + orbit_radius,
            ],
            outline=(80, 200, 120),
            width=3,
        )

        draw.ellipse(
            [
                right_center_x - subject_r,
                center_y - subject_r,
                right_center_x + subject_r,
                center_y + subject_r,
            ],
            fill=(220, 220, 220),
        )

        angle_rad = math.radians(orbit * 45 - 90)
        cam_x = right_center_x + orbit_radius * math.cos(angle_rad)
        cam_y = center_y + orbit_radius * math.sin(angle_rad)

        draw.ellipse(
            [cam_x - 6, cam_y - 6, cam_x + 6, cam_y + 6],
            fill=(100, 180, 255),
        )

        return img

    def _pil_to_comfy_image(self, pil_img):
        np_img = np.array(pil_img).astype(np.float32) / 255.0
        tensor = torch.from_numpy(np_img)
        return [tensor]


NODE_CLASS_MAPPINGS = {
    "CameraAnglePromptBuilder": CameraAnglePromptBuilder
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CameraAnglePromptBuilder": "Camera Angle Prompt Builder (Orbit + Pitch + Zoom)"
}
