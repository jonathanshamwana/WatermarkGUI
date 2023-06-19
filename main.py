from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont

# List of file types the user can upload
f_types = [('Jpg Files', '*.jpg'),('PNG Files','*.png')]

# Create the window
window = Tk()
window.title("Add Watermarks")
window.geometry("700x700")
window.config(padx=20, pady=20)

# Create Canvas
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="new_watermark.png")
canvas.create_image(100,100,image=logo_img)
canvas.grid(column=1, row=2, columnspan=2)

# Create the heading
heading = Label(text="Add a watermark to your image", font=("Arial", 24, "bold"))
heading.grid(row=0, column=1, pady=20, columnspan=1)

# Function for adding the watermark to the image
def add_watermark():

    watermark_text = name_entry.get()
    file_path = filedialog.askopenfilename(filetypes=f_types)
    image = Image.open(file_path)

    # Calculate the appropriate font size
    base_font_size = 36
    image_width, image_height = image.size
    slider_value = size_slider.get()
    font_size = int(base_font_size * min(image_width / 800, image_height / 500) / (2 ** (3 - slider_value)))

    # Create a transparent layer that the text can be written
    watermark_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    font = ImageFont.truetype("Arial.ttf", font_size)
    draw = ImageDraw.Draw(watermark_layer)

    # Calculate where the watermark will go
    position = radio_state.get()
    text_width, text_height = draw.textsize(watermark_text, font)
    if position == 1:
        x = 0
        y = 0
    elif position == 2:
        x = image.width - text_width
        y = 0
    elif position == 3:
        x = 0
        y = image.height - text_height
    elif position == 4:
        x = image.width - text_width
        y = image.height - text_height
    if position == 5:
        x = (image.width - text_width) // 2
        y = (image.height - text_height) // 2

    # Writes the text onto the watermark layer
    draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))

    # Combine the image and the watermark layer
    watermarked_image = Image.alpha_composite(image.convert("RGBA"), watermark_layer)

    # Save the watermarked image
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if save_path:
        watermarked_image.save(save_path)
        print("Image saved successfully!")

# Field for uploading your watermark text
name_label = Label(text="Watermark Text:", font=("Arial", 12), justify="right")
name_label.grid(row=3, column=0, pady=20)
name_entry = Entry(width=30, font=("Arial", 12))
name_entry.grid(row=3, column=1, columnspan=2, pady=20)

# Ask user where they'd like the watermark
position_label = Label(text="Position", font=("Arial", 12))
position_label.grid(row=5, column=1, pady=10)
radio_state = IntVar()
radio1 = Radiobutton(text="Top left", value=1, variable=radio_state, font=("Arial", 10))
radio2 = Radiobutton(text="Top right", value=2, variable=radio_state, font=("Arial", 10))
radio3 = Radiobutton(text="Bottom left", value=3, variable=radio_state, font=("Arial", 10))
radio4 = Radiobutton(text="Bottom right", value=4, variable=radio_state, font=("Arial", 10))
radio5 = Radiobutton(text="Center", value=5, variable=radio_state, font=("Arial", 10))
radio1.grid(row=6, column=1)
radio2.grid(row=7, column=1)
radio3.grid(row=8, column=1)
radio4.grid(row=9, column=1)
radio5.grid(row=10, column=1)

# Ask user how big the watermark should be
size_label = Label(text="Size")
size_slider = Scale(from_=1, to=3, orient=HORIZONTAL)
size_label.grid(row=11, column=1, pady=(20, 0), sticky="n")
size_slider.grid(row=12, column=1, pady=(0,20))

# Submit button
submit_button = Button(text="Upload Image", command=add_watermark, font=("Arial", 14, "bold"))
submit_button.grid(row=13, column=1, pady=20, columnspan=1)

window.mainloop()

