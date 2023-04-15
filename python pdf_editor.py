import fitz
import PySimpleGUI as sg

# Define the GUI layout
layout = [
    [sg.Text('PDF File:'), sg.Input(key='-FILE-'), sg.FileBrowse()],
    [sg.Text('Page Number:'), sg.Input(key='-PAGE-')],
    [sg.Button('Rotate Left'), sg.Button('Rotate Right'), sg.Button('Cut'), sg.Button('Save As'), sg.Button('Exit')],
    [sg.Text('Page Preview:')],
    [sg.Image(key='-PREVIEW-')],
    [sg.Text('Page Thumbnails:')],
    [sg.Listbox(values=[], size=(20, 10), key='-THUMBNAILS-')]
]

# Create the GUI window
window = sg.Window('PDF Editor', layout)

# Main event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    elif event == 'Cut':
        # Open the PDF file
        pdf_file = fitz.open(values['-FILE-'])
        # Get the page number to cut
        page_num = int(values['-PAGE-']) - 1
        # Cut the page
        pdf_file.delete_page(page_num)
        # Save the modified PDF file
        pdf_file.saveIncr()
        # Close the PDF file
        pdf_file.close()
        sg.popup('Page cut successfully!')
    elif event == 'Rotate Left':
        # Open the PDF file
        pdf_file = fitz.open(values['-FILE-'])
        # Get the page number to rotate
        page_num = int(values['-PAGE-']) - 1
        # Rotate the page left
        page = pdf_file[page_num]
        page.set_rotation(page.rotation - 90)
        # Save the modified PDF file
        pdf_file.saveIncr()
        # Close the PDF file
        pdf_file.close()
        # Display a message to the user
        sg.popup('Page rotated left successfully!')
    elif event == 'Rotate Right':
        # Open the PDF file
        pdf_file = fitz.open(values['-FILE-'])
        # Get the page number to rotate
        page_num = int(values['-PAGE-']) - 1
        # Rotate the page right
        page = pdf_file[page_num]
        page.set_rotation(page.rotation + 90)
        # Save the modified PDF file
        pdf_file.saveIncr()
        # Close the PDF file
        pdf_file.close()
        # Display a message to the user
        sg.popup('Page rotated right successfully!')
    elif event == 'Save As':
        # Open the PDF file
        pdf_file = fitz.open(values['-FILE-'])
        # Get the file name to save as
        save_file = sg.popup_get_file('Save As', save_as=True)
        if save_file:
            # Save the PDF file with the new name
            pdf_file.save(save_file)
            # Display a message to the user
            sg.popup('File saved successfully!')
        # Close the PDF file
        pdf_file.close()
    else:
        # Update the page preview and thumbnails
        try:
            # Open the PDF file
            pdf_file = fitz.open(values['-FILE-'])
            # Get the page number to preview
            page_num = int(values['-PAGE-']) - 1
            # Get the page object
            page = pdf_file[page_num]
            # Apply any modifications to the page
            if page.rotation != 0:
                page.apply_transform()
            # Render the page as an image
            pix = page.get_pixmap()
            # Convert the image to bytes
            img_bytes = pix.tobytes()
            # Update the image in the GUI window
            window['-PREVIEW-'].update(data=img_bytes)
            # Get the number of pages in the PDF file
            num_pages = len(pdf_file)
            # Create a list of page thumbnails
            thumbnails = []
            for i in range(num_pages):        
            # Get the page object
                page = pdf_file[i]
            # Apply any modifications to the page
            if page.rotation != 0:
                page.apply_transform()
            # Render the page as an image
            pix = page.get_pixmap()
            # Convert the image to bytes
            img_bytes = pix.tobytes()
            # Add the thumbnail to the list
            thumbnails.append(img_bytes)
            # Update the listbox in the GUI window
            window['-THUMBNAILS-'].update(values=thumbnails)
            # Close the PDF file
            pdf_file.close()
        except:
         # Clear the page preview and thumbnails
         window['-PREVIEW-'].update(data=None)
         window['-THUMBNAILS-'].update(values=[])