# 🎮 Minecraft-Style Nametag Headtracker

> *Ever wanted to feel like you're in Minecraft IRL? Well, now you can!* ⛏️

## ✨ What is this sorcery?

This magical piece of code turns your webcam into a Minecraft-like experience by floating a nametag above your head - just like in the game! It tracks your face in real-time and displays your name with the authentic Minecraft font. How cool is that? 🎯

## 🎥 Features

-  Floating nametag that follows your head movements
-  Authentic Minecraft font styling
-  Smooth motion tracking
-  Real-time FPS counter
-  Smart background detection for text visibility
-  Works with any webcam

## 🛠️ Requirements

- Python 3.6+
- OpenCV (`cv2`)
- Mediapipe
- NumPy
- PIL (Python Imaging Library)
- A webcam that works! 
- Your face 

## 📦 Installation

1. Clone this repository:
```bash
git clone https://github.com/kguba/Minecraft_Nametag_Headtracker.git
```

2. Install the required packages:
```bash
pip install opencv-python mediapipe numpy pillow
```

3. Make sure you have the Minecraft font file (`minecraft_font.ttf`) in the same directory as the script!

## 🎮 How to Use

1. Run the script:
```bash
python nametag_headtracker.py
```

2. Strike a pose! 🕺💃
   - The nametag will automagically appear above your head
   - Move around to see it follow you
   - Press 'q' to quit 

## ⚙️ Customization

Want to make it your own? Here's how:

```python
# Change your display name
floating_text = "YourCoolNameHere"

# Adjust the font size
font_size = 48  # Make it bigger or smaller!

# Tweak the smoothing for movement
smoothing_factor = 0.5  # Higher = smoother but slower
```

## 🎯 Pro Tips

- Keep your whole face in the frame for best tracking
- Good lighting helps the tracker see you better
- Try different names and font sizes for maximum fun!
- Dance around to test the smooth tracking (we won't judge 🕺)

## 🐛 Troubleshooting

- Can't see the nametag? Make sure your face is fully visible!
- Text looking weird? Check if the Minecraft font file is in the right place
- Camera not working? Try changing the camera index in `cv2.VideoCapture(0)`
- Still having issues? Try turning it off and on again 

## 🎨 Behind the Scenes

This project uses:
- MediaPipe for super-accurate face detection
- OpenCV for video capture and display
- PIL for fancy text rendering
- Math and magic for smooth tracking 

## 🎉 Credits

- Minecraft font and style inspiration: Mojang (Thanks for the awesome game!)
- Your face: You (Thanks for being awesome!)

## 📝 License

Feel free to use this for fun! Just remember to credit the original project if you share it.

---

Made with ❤️ and a bit of redstone dust ⚡

*Remember: You're always in Creative mode when coding!* 🎮✨ 
