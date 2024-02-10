import cv2
import numpy as np

import telebot
import os

TOKEN = '6744137063:AAEPa39lLrWyxOD5XAEM_Mvtr8I6GzhI94I'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Отправь фотографию БЕЗ СЖАТИЯ!")


@bot.message_handler(content_types=['document'])
def document(message):
    try:
        # Check if the document is an image
        if 'image' in message.document.mime_type:
            file_id = message.document.file_id
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            user_id = message.from_user.id
            directory = f'img/'
            os.makedirs(directory, exist_ok=True)  # Ensure the directory exists
            with open(f'{directory}/{user_id}.png', 'wb') as new_file:
                new_file.write(downloaded_file)

            create_final_photo('img/photo.png', 'img/screenshot.png', [
                (315, 931), (1799, 1020), (354, 1818), (1797, 1714)    # Alina's photo coords
            ], user_id)

            with open(f'img/{user_id}.jpg', 'rb') as image:
                bot.send_document(message.chat.id, image)

            bot.reply_to(message, "Image saved successfully.")
        else:
            bot.reply_to(message, "Please send an image file.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")


def create_final_photo(original_img_path: str, screenshot_img_path: str, screen_coords: list[tuple[int, int]], user_id: int):
    # Load the original image and the screenshot
    original_img = cv2.imread(original_img_path)
    screenshot_img = cv2.imread(screenshot_img_path)

    # Define the points where the screenshot will be placed in the original image
    pts1 = np.float32([[0, 0], [screenshot_img.shape[1], 0], [0, screenshot_img.shape[0]], [screenshot_img.shape[1], screenshot_img.shape[0]]])
    pts2 = np.float32(screen_coords)

    # Calculate the transformation matrix and apply it to the screenshot
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    transformed_screenshot = cv2.warpPerspective(screenshot_img, matrix, (original_img.shape[1], original_img.shape[0]))

    # Create a mask to combine the images
    mask = np.zeros_like(original_img, dtype=np.uint8)
    cv2.fillPoly(mask, [np.int32(pts2)], (255, 255, 255))
    inv_mask = cv2.bitwise_not(mask)

    # Combine the original image and the transformed screenshot
    img_with_mask = cv2.bitwise_and(original_img, inv_mask)
    final_img = cv2.bitwise_or(img_with_mask, transformed_screenshot)

    # Set JPEG quality level to 95 for high quality
    compression_parameters = [cv2.IMWRITE_JPEG_QUALITY, 95]

    # Save the final image as JPEG
    cv2.imwrite(f'img/{user_id}.jpg', final_img, compression_parameters)


if __name__ == '__main__':
    bot.polling()

# # laptop screen cords (top-left, top-right, bottom-left, bottom-right)
# monitor_coords = [(315, 931), (1799, 1020), (354, 1818), (1797, 1714)]
#
#
# # Paths to your images
# photo_path = 'img/photo.png'
# screenshot_path = 'img/screenshot.png'
#
# overlay_screenshot(photo_path, screenshot_path, monitor_coords)
