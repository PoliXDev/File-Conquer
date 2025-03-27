File Converter

A file conversion application with a graphical interface developed in PyQt5.

Main Features
Text and Documents
Convert Excel to CSV

Convert Word to PDF

Images and Graphics
Convert JPG to PDF

Convert PNG to PDF

Convert JPG to PNG

Convert PNG to JPG

Convert PNG to AVIF

Convert PNG to SVG

Convert WEBP to PNG

Convert AVIF to PNG

Convert SVG to PNG

Convert SVG to PDF

Requirements
Python 3.6+

PyQt5

pandas

docx2pdf

Pillow (PIL)

numpy

potrace (for SVG conversion)

Installation
bash
Copiar
Editar
pip install PyQt5 pandas docx2pdf pillow numpy
pip install pypotrace  # For PNG to SVG conversion
Setup
To properly display background images in the program:

Create a folder named assets in the project directory.

Place all image files inside the assets folder.

Ensure the main program file is located outside the assets folder, in the project's root directory.

User Interface
The application features a modern and user-friendly interface, including:

Startup screen with animation

Conversion type selector organized by categories

Input/output file selection

Progress bar to track conversion

Status messages with visual feedback

Developed by: Daniel Ruiz Poli
Academy: ConquerBlocks

Version
3.9
Date: March 2024
