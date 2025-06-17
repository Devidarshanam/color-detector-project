import cv2
import pandas as pd

# Load color data
colors = pd.read_csv('colors.csv')

# Get closest color name from RGB
def get_color_name(R, G, B):
    min_dist = float('inf')
    cname = ""
    for i in range(len(colors)):
        r, g, b = int(colors.loc[i, 'red']), int(colors.loc[i, 'green']), int(colors.loc[i, 'blue'])
        d = abs(R - r) + abs(G - g) + abs(B - b)
        if d < min_dist:
            min_dist = d
            cname = colors.loc[i, 'name']
    return cname

# Decide whether text should be black or white based on brightness
def get_text_color(r, g, b):
    brightness = (r * 299 + g * 587 + b * 114) / 1000  # standard luminance formula
    return (0, 0, 0) if brightness > 150 else (255, 255, 255)  # black if bright, else white

# Mouse click event
clicked = False
r = g = b = xpos = ypos = 0
color_text = ""

def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked, color_text
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True
        xpos = x
        ypos = y
        b, g, r = frame[y, x]
        b, g, r = int(b), int(g), int(r)
        color_text = get_color_name(r, g, b) + f" R={r} G={g} B={b}"

# Start webcam
cap = cv2.VideoCapture(0)
cv2.namedWindow('Color Detector')
cv2.setMouseCallback('Color Detector', draw_function)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if clicked:
        # Draw background rectangle
        cv2.rectangle(frame, (20, 20), (750, 60), (b, g, r), -1)
        # Choose best text color
        text_color = get_text_color(r, g, b)
        # Display text
        cv2.putText(frame, color_text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, text_color, 2, cv2.LINE_AA)

    cv2.imshow('Color Detector', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
