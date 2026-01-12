# Camera Angle Prompt Builder (ComfyUI)

A custom ComfyUI node that turns **camera intent into deterministic prompts**, with a visual camera diagram you can read at a glance.

Instead of typing camera language by hand, you adjust **Orbit, Pitch, and Zoom** using sliders and let the node generate a clean, repeatable prompt string.

The demo subject used here is **Battle Goose**, because if you are going to teach cinematic dominance, you might as well do it properly.

---

## What this node does

This node:

* Generates a camera-aware prompt string based on slider inputs
* Outputs a visual camera diagram showing camera position and height
* Keeps camera grammar consistent and reproducible
* Works for still images or video workflows
* Runs entirely inside ComfyUI with no external UI dependencies

It is designed to feel like blocking a camera, not writing text.

---

## Camera controls

The node exposes three sliders that map directly to cinematic concepts.

### Orbit

Controls the camera position around the subject.

Values progress in 45 degree steps:

* front
* front-right quarter
* right side
* back-right quarter
* back
* back-left quarter
* left side
* front-left quarter

This is your horizontal camera orbit.

---

### Pitch

Controls the vertical camera height and dominance.

* low-angle shot
* eye-level shot
* elevated shot
* high-angle shot

This affects how powerful or diminished the subject feels.

---

### Zoom

Controls framing scale.

* close-up
* medium shot
* wide shot

This is treated as conceptual framing rather than optical focal length.

---

## Outputs

The node produces two outputs.

### Prompt (STRING)

A fully assembled prompt such as:

```
<sks> back-right quarter view low-angle shot medium shot
```

This plugs directly into CLIP Text Encode or any prompt-based workflow.

---

### Camera Diagram (IMAGE)

A generated diagram showing:

* Left panel: side profile view

  * ground plane
  * subject
  * camera height relative to subject

* Right panel: top-down orbit view

  * subject at center
  * camera position on orbit ring

This updates live as you adjust sliders.

It is meant to be read instantly.

---

## Example workflow with Battle Goose

In the provided example workflow, the **Camera Angle Prompt Builder** lives inside a **subgraph**.

Inside the subgraph:

* The node sliders are exposed as subgraph widgets
* A Preview Image node shows the camera diagram
* The prompt output feeds back to the main graph

This keeps the main workflow clean while making camera controls always visible.

You adjust camera intent without digging through the graph.

---

## Demo subject: Battle Goose

The example uses an image of a goose known internally as **Battle Goose**.

This is intentional.

Battle Goose makes camera changes obvious and funny:

* Low angle makes the goose absurdly heroic
* High angle makes it feel defeated
* Orbiting the goose reads instantly
* Zoom exaggerates dominance or comedy

It is impossible to ignore and perfect for demos.

---

## Why use this instead of typing prompts

* Prevents camera language drift
* Encourages intentional framing
* Makes shot continuity possible
* Scales to video workflows
* Teaches camera grammar visually

You are not guessing what the model will interpret.
You are telling it exactly how the camera is positioned.

---

## Installation

1. Copy the folder into your ComfyUI custom_nodes directory:

```
ComfyUI/custom_nodes/camera_prompt_builder/
```

2. Restart ComfyUI

3. Find the node under:

```
Prompt / Camera
```

---

## Intended use cases

* Cinematic character portraits
* Consistent camera angles across generations
* Video shot planning
* Teaching camera fundamentals
* Making a goose look terrifying

---

## Notes

* The IMAGE output is compatible with Preview Image
* The node outputs a single image batch, as required by ComfyUI
* No frontend modifications are required
* No Three.js or web UI is used

---

## Future ideas

Possible extensions include:

* Camera presets
* Orbit animation for video
* Metadata outputs for external tools
* JSON export of camera state

But the current version is intentionally simple and stable.

---

## Final word

If Battle Goose looks intimidating from a low angle,
the node is doing its job.

Enjoy.
