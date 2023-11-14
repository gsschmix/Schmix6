import tkinter as tk


# this function is used to create a frame that will hold the documentation
# for the program
def doc(win1, letter_color):
    documents = tk.Frame(win1, bg="#262629", width=900, height=650,
                         borderwidth=5, relief="raised")
    documents.grid(column=1, row=0, pady=20)
    documents.grid_propagate(False)

    # open text file to get documentation
    f = open("READ_ME.txt", "r")

    # read the contents of the file
    content = f.read()

    # create a label for Documentation
    tk.Label(documents, bg=documents["bg"], fg=letter_color,
             text="Documentation", font=('Castellar', 50))\
        .grid(column=0, row=0)

    # create a text area to hold the content of the file
    txt_area = tk.Text(documents, bg="black", fg="cyan")
    txt_area.insert(tk.END, content)

    # close the file
    f.close()

    # put the text area on the grid
    txt_area.grid(column=0, row=1)

    # raise the frame above any other frames
    documents.tkraise()
