import cv2
import numpy as np
import xlsxwriter


def create_mosaic_in_excel(photo, box_height, box_width, col_width=2, row_height=15):
    # Get the height and width of the photo
    height, width, _ = photo.shape

    # Create Excel workbook and worksheet
    workbook = xlsxwriter.Workbook('photo-mosaic.xlsx')
    worksheet = workbook.add_worksheet("own-pic")

    # Resize columns and rows
    worksheet.set_column(0, width // box_width - 1, col_width)
    for i in range(height // box_height):
        worksheet.set_row(i, row_height)

    # Create mosaic
    for i in range(0, height, box_height):
        for j in range(0, width, box_width):
            # Create region of interest (ROI)
            roi = photo[i:i + box_height, j:j + box_width]
            # Use numpy to calculate mean in ROI of color channels
            b_mean = np.mean(roi[:, :, 0])
            g_mean = np.mean(roi[:, :, 1])
            r_mean = np.mean(roi[:, :, 2])

            # Convert mean to int
            b_mean_int = b_mean.astype(int).item()
            g_mean_int = g_mean.astype(int).item()
            r_mean_int = r_mean.astype(int).item()

            # Create color code
            color = '#{:02x}{:02x}{:02x}'.format(r_mean_int, g_mean_int, b_mean_int)

            # Add color code to cell
            cell_format = workbook.add_format()
            cell_format.set_bg_color(color)
            worksheet.write(i // box_height, j // box_width, "", cell_format)

    # Close and write the Excel sheet
    workbook.close()


def main():
    try:
        photo = cv2.imread("covpic.png")
    except OSError:
        print("The file is not found")
        exit()
    number_cols = 50
    number_rows = 50

    # Get height and width of photo
    height, width, _ = photo.shape
    box_width = width // number_cols
    box_height = height // number_rows

    # To make sure that it we can slice the photo in box-sizes
    width = (width // box_width) * box_width
    height = (height // box_height) * box_height
    photo = cv2.resize(photo, (width, height))

    # Create the Excel mosaic
    create_mosaic_in_excel(photo.copy(), box_height, box_width, col_width=2, row_height=15)
    print("File written successfully")


main()
