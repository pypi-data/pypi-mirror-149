import cv2

from skcvideo.colors import WHITE


DEFAULT_FONT = cv2.FONT_HERSHEY_SIMPLEX



def put_text(img, text, org, fontFace=DEFAULT_FONT, fontScale=1.0, color=WHITE,
        thickness=1, lineType=cv2.LINE_AA, align_x='center', align_y='center'):
    x, y = org
    (w, h), _ = cv2.getTextSize(text, fontFace, fontScale, thickness)

    if align_x == 'left':
        org_x = x
    elif align_x == 'center':
        org_x = x - w // 2
    elif align_x == 'right':
        org_x = x - w

    if align_y == 'bottom':
        org_y = y
    elif align_y == 'center':
        org_y = y + h // 2
    elif align_y == 'top':
        org_y = y + h

    cv2.putText(
        img=img,
        text=text,
        org=(org_x, org_y),
        fontFace=fontFace,
        fontScale=fontScale,
        color=color,
        thickness=thickness,
        lineType=lineType,
    )
