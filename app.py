# # # import streamlit as st
# # # import os
# # # from pathlib import Path
# # # import ffmpeg
# # # from PIL import Image
# # # import io
# # # import base64
# # # from PyPDF2 import PdfReader, PdfWriter
# # # from pdf2docx import Converter as Pdf2DocxConverter
# # # from docx import Document
# # # from docx2pdf import convert as docx2pdf_convert
# # # from pdf2image import convert_from_path
# # # import zipfile
# # # import traceback

# # # # Force Poppler into PATH
# # # os.environ["PATH"] += os.pathsep + r"C:\poppler-24.08.0\bin"  # Adjust if your Poppler path differs

# # # # Supported file extensions
# # # EXTENSIONS = {
# # #     "image": ["jpg", "jpeg", "png", "gif", "bmp", "webp", "ico", "tif", "tiff"],
# # #     "video": ["mp4", "m4v", "3gp", "avi", "mov", "wmv", "mkv", "flv", "webm"],
# # #     "audio": ["mp3", "wav", "ogg", "aac", "wma", "flac", "m4a"],
# # #     "document": ["pdf", "docx"],
# # # }

# # # # Utility functions
# # # def get_file_extension(file_name):
# # #     return Path(file_name).suffix[1:].lower()

# # # def remove_file_extension(file_name):
# # #     return Path(file_name).stem

# # # def bytes_to_size(bytes_size):
# # #     sizes = ["Bytes", "KB", "MB", "GB", "TB"]
# # #     if bytes_size == 0:
# # #         return "0 Byte"
# # #     i = min(int((len(str(bytes_size)) - 1) // 3), 4)
# # #     size = bytes_size / (1024 ** i)
# # #     return f"{size:.2f} {sizes[i]}"

# # # def convert_file(input_file, input_ext, output_ext):
# # #     output_base = remove_file_extension(input_file.name)
# # #     output_filename = f"{output_base}.{output_ext}"
# # #     output_path = Path(output_filename)

# # #     try:
# # #         # Save the uploaded file temporarily
# # #         with open(input_file.name, "wb") as f:
# # #             f.write(input_file.read())

# # #         if input_ext in EXTENSIONS["image"] and output_ext in EXTENSIONS["image"]:
# # #             # Image to Image
# # #             img = Image.open(input_file.name)
# # #             if output_ext == "jpg":
# # #                 img.save(output_path, format="JPEG", quality=95)
# # #             else:
# # #                 img.save(output_path, format=output_ext.upper())
# # #         elif input_ext in EXTENSIONS["video"] or input_ext in EXTENSIONS["audio"]:
# # #             # Video/audio
# # #             stream = ffmpeg.input(input_file.name)
# # #             if output_ext == "3gp":
# # #                 stream = ffmpeg.output(
# # #                     stream, output_filename,
# # #                     r=20, s="352x288", vb="400k",
# # #                     acodec="aac", strict="experimental",
# # #                     ac=1, ar=8000, ab="24k"
# # #                 )
# # #             else:
# # #                 stream = ffmpeg.output(stream, output_filename)
# # #             ffmpeg.run(stream, overwrite_output=True)
# # #         elif input_ext == "docx":
# # #             if output_ext == "pdf":
# # #                 # Word to PDF
# # #                 docx2pdf_convert(input_file.name, output_filename)
# # #             elif output_ext in ["jpg", "png"]:
# # #                 # Word to JPG/PNG
# # #                 temp_pdf = f"{output_base}_temp.pdf"
# # #                 docx2pdf_convert(input_file.name, temp_pdf)
# # #                 images = convert_from_path(temp_pdf, dpi=300)
# # #                 if len(images) == 1:
# # #                     if output_ext == "jpg":
# # #                         images[0].save(output_path, format="JPEG", quality=95)
# # #                     else:
# # #                         images[0].save(output_path, format="PNG")
# # #                 else:
# # #                     # Zip multiple pages
# # #                     zip_filename = f"{output_base}.zip"
# # #                     with zipfile.ZipFile(zip_filename, 'w') as zipf:
# # #                         for i, img in enumerate(images):
# # #                             img_path = f"{output_base}_page_{i+1}.{output_ext}"
# # #                             if output_ext == "jpg":
# # #                                 img.save(img_path, format="JPEG", quality=95)
# # #                             else:
# # #                                 img.save(img_path, format="PNG")
# # #                             zipf.write(img_path)
# # #                             os.remove(img_path)
# # #                     output_path = Path(zip_filename)
# # #                 os.remove(temp_pdf)
# # #         elif input_ext == "pdf":
# # #             if output_ext == "docx":
# # #                 # PDF to Word
# # #                 cv = Pdf2DocxConverter(input_file.name)
# # #                 cv.convert(output_filename)
# # #                 cv.close()
# # #             elif output_ext in ["jpg", "png"]:
# # #                 # PDF to JPG/PNG
# # #                 images = convert_from_path(input_file.name, dpi=300)
# # #                 if len(images) == 1:
# # #                     if output_ext == "jpg":
# # #                         images[0].save(output_path, format="JPEG", quality=95)
# # #                     else:
# # #                         images[0].save(output_path, format="PNG")
# # #                 else:
# # #                     # Zip multiple pages
# # #                     zip_filename = f"{output_base}.zip"
# # #                     with zipfile.ZipFile(zip_filename, 'w') as zipf:
# # #                         for i, img in enumerate(images):
# # #                             img_path = f"{output_base}_page_{i+1}.{output_ext}"
# # #                             if output_ext == "jpg":
# # #                                 img.save(img_path, format="JPEG", quality=95)
# # #                             else:
# # #                                 img.save(img_path, format="PNG")
# # #                             zipf.write(img_path)
# # #                             os.remove(img_path)
# # #                     output_path = Path(zip_filename)
# # #             elif output_ext == "pdf":
# # #                 # PDF to PDF
# # #                 reader = PdfReader(input_file.name)
# # #                 writer = PdfWriter()
# # #                 for page in reader.pages:
# # #                     writer.add_page(page)
# # #                 with open(output_filename, "wb") as f:
# # #                     writer.write(f)
# # #         else:
# # #             raise ValueError("Conversion not supported.")

# # #         return output_path
# # #     except Exception as e:
# # #         st.error(f"Error converting file: {str(e)}\n\nDetails: {traceback.format_exc()}")
# # #         return None
# # #     finally:
# # #         if os.path.exists(input_file.name):
# # #             os.remove(input_file.name)

# # # def get_binary_file_downloader_html(file_path, file_label="File"):
# # #     with open(file_path, "rb") as f:
# # #         data = f.read()
# # #     b64 = base64.b64encode(data).decode()
# # #     href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}">Download {file_label}</a>'
# # #     return href

# # # # Streamlit app
# # # st.set_page_config(page_title="Modifio - Free Unlimited File Converter", layout="wide")

# # # st.header("Free Unlimited File Converter")
# # # st.write("""
# # #     Unleash your creativity with Modifio – the ultimate online tool for unlimited and free multimedia and document conversion.
# # #     Transform images, audio, videos, PDFs, and Word files into PDF, Word, JPG, or PNG formats. Multi-page PDFs/Word docs are zipped as images.
# # # """)

# # # # File uploader
# # # uploaded_file = st.file_uploader("Upload a file", type=sum(EXTENSIONS.values(), []))

# # # if uploaded_file:
# # #     file_ext = get_file_extension(uploaded_file.name)
# # #     file_size = bytes_to_size(uploaded_file.size)
# # #     st.write(f"**File:** {uploaded_file.name} ({file_size})")

# # #     # Determine available output formats
# # #     if file_ext in EXTENSIONS["image"]:
# # #         output_options = EXTENSIONS["image"]
# # #     elif file_ext in EXTENSIONS["video"]:
# # #         output_options = EXTENSIONS["video"] + EXTENSIONS["audio"]
# # #     elif file_ext in EXTENSIONS["audio"]:
# # #         output_options = EXTENSIONS["audio"]
# # #     elif file_ext == "docx":
# # #         output_options = ["pdf", "jpg", "png"]
# # #     elif file_ext == "pdf":
# # #         output_options = ["docx", "jpg", "png", "pdf"]
# # #     else:
# # #         st.error("Unsupported file type.")
# # #         output_options = []

# # #     if output_options:
# # #         output_format = st.selectbox("Convert to", output_options, index=None, placeholder="Select format...")
        
# # #         if st.button("Convert Now") and output_format:
# # #             with st.spinner("Converting..."):
# # #                 result = convert_file(uploaded_file, file_ext, output_format)
                
# # #                 if result:
# # #                     st.success("Conversion complete!")
# # #                     if result.suffix in [".zip"]:
# # #                         st.info("Multi-page document converted to a ZIP file containing images.")
# # #                     st.markdown(get_binary_file_downloader_html(result, "Converted File"), unsafe_allow_html=True)
# # #                     if os.path.exists(result):
# # #                         os.remove(result)

# # # st.markdown("---")
# # # st.write("Built with ❤️ by SOUHAIL BEN-LHACHEMI | [Github Repo](https://github.com/benlhachemi/modifio.git)")
# # import streamlit as st
# # import os
# # from pathlib import Path
# # import ffmpeg
# # from PIL import Image
# # import io
# # import base64
# # from PyPDF2 import PdfReader, PdfWriter
# # from pdf2docx import Converter as Pdf2DocxConverter
# # from docx import Document
# # from docx2pdf import convert as docx2pdf_convert
# # from pdf2image import convert_from_path
# # import zipfile
# # import traceback

# # # Set page config as the first Streamlit command
# # st.set_page_config(page_title="SamDocAI - File Converter", layout="wide")

# # # Force Poppler into PATH
# # os.environ["PATH"] += os.pathsep + r"C:\poppler-24.08.0\bin"  # Adjust if your Poppler path differs

# # # Supported file extensions
# # EXTENSIONS = {
# #     "image": ["jpg", "jpeg", "png", "gif", "bmp", "webp", "ico", "tif", "tiff"],
# #     "video": ["mp4", "m4v", "3gp", "avi", "mov", "wmv", "mkv", "flv", "webm"],
# #     "audio": ["mp3", "wav", "ogg", "aac", "wma", "flac", "m4a"],
# #     "document": ["pdf", "docx"],
# # }

# # # Utility functions
# # def get_file_extension(file_name):
# #     return Path(file_name).suffix[1:].lower()

# # def remove_file_extension(file_name):
# #     return Path(file_name).stem

# # def bytes_to_size(bytes_size):
# #     sizes = ["Bytes", "KB", "MB", "GB", "TB"]
# #     if bytes_size == 0:
# #         return "0 Byte"
# #     i = min(int((len(str(bytes_size)) - 1) // 3), 4)
# #     size = bytes_size / (1024 ** i)
# #     return f"{size:.2f} {sizes[i]}"

# # def convert_file(input_file, input_ext, output_ext):
# #     output_base = remove_file_extension(input_file.name)
# #     output_filename = f"{output_base}.{output_ext}"
# #     output_path = Path(output_filename)

# #     try:
# #         with open(input_file.name, "wb") as f:
# #             f.write(input_file.read())

# #         if input_ext in EXTENSIONS["image"] and output_ext in EXTENSIONS["image"]:
# #             img = Image.open(input_file.name)
# #             if output_ext == "jpg":
# #                 img.save(output_path, format="JPEG", quality=95)
# #             else:
# #                 img.save(output_path, format=output_ext.upper())
# #         elif input_ext in EXTENSIONS["video"] or input_ext in EXTENSIONS["audio"]:
# #             stream = ffmpeg.input(input_file.name)
# #             if output_ext == "3gp":
# #                 stream = ffmpeg.output(
# #                     stream, output_filename,
# #                     r=20, s="352x288", vb="400k",
# #                     acodec="aac", strict="experimental",
# #                     ac=1, ar=8000, ab="24k"
# #                 )
# #             else:
# #                 stream = ffmpeg.output(stream, output_filename)
# #             ffmpeg.run(stream, overwrite_output=True)
# #         elif input_ext == "docx":
# #             if output_ext == "pdf":
# #                 docx2pdf_convert(input_file.name, output_filename)
# #             elif output_ext in ["jpg", "png"]:
# #                 temp_pdf = f"{output_base}_temp.pdf"
# #                 docx2pdf_convert(input_file.name, temp_pdf)
# #                 images = convert_from_path(temp_pdf, dpi=300)
# #                 if len(images) == 1:
# #                     if output_ext == "jpg":
# #                         images[0].save(output_path, format="JPEG", quality=95)
# #                     else:
# #                         images[0].save(output_path, format="PNG")
# #                 else:
# #                     zip_filename = f"{output_base}.zip"
# #                     with zipfile.ZipFile(zip_filename, 'w') as zipf:
# #                         for i, img in enumerate(images):
# #                             img_path = f"{output_base}_page_{i+1}.{output_ext}"
# #                             if output_ext == "jpg":
# #                                 img.save(img_path, format="JPEG", quality=95)
# #                             else:
# #                                 img.save(img_path, format="PNG")
# #                             zipf.write(img_path)
# #                             os.remove(img_path)
# #                     output_path = Path(zip_filename)
# #                 os.remove(temp_pdf)
# #         elif input_ext == "pdf":
# #             if output_ext == "docx":
# #                 cv = Pdf2DocxConverter(input_file.name)
# #                 cv.convert(output_filename)
# #                 cv.close()
# #             elif output_ext in ["jpg", "png"]:
# #                 images = convert_from_path(input_file.name, dpi=300)
# #                 if len(images) == 1:
# #                     if output_ext == "jpg":
# #                         images[0].save(output_path, format="JPEG", quality=95)
# #                     else:
# #                         images[0].save(output_path, format="PNG")
# #                 else:
# #                     zip_filename = f"{output_base}.zip"
# #                     with zipfile.ZipFile(zip_filename, 'w') as zipf:
# #                         for i, img in enumerate(images):
# #                             img_path = f"{output_base}_page_{i+1}.{output_ext}"
# #                             if output_ext == "jpg":
# #                                 img.save(img_path, format="JPEG", quality=95)
# #                             else:
# #                                 img.save(img_path, format="PNG")
# #                             zipf.write(img_path)
# #                             os.remove(img_path)
# #                     output_path = Path(zip_filename)
# #             elif output_ext == "pdf":
# #                 reader = PdfReader(input_file.name)
# #                 writer = PdfWriter()
# #                 for page in reader.pages:
# #                     writer.add_page(page)
# #                 with open(output_filename, "wb") as f:
# #                     writer.write(f)
# #         else:
# #             raise ValueError("Conversion not supported.")

# #         return output_path
# #     except Exception as e:
# #         st.error(f"Error converting file: {str(e)}\n\nDetails: {traceback.format_exc()}")
# #         return None
# #     finally:
# #         if os.path.exists(input_file.name):
# #             os.remove(input_file.name)

# # def get_binary_file_downloader_html(file_path, file_label="File"):
# #     with open(file_path, "rb") as f:
# #         data = f.read()
# #     b64 = base64.b64encode(data).decode()
# #     href = f'<a href="data:application/octet-stream;base64,{b64}" download="{os.path.basename(file_path)}">Download {file_label}</a>'
# #     return href

# # # Custom CSS for beautiful UI
# # st.markdown("""
# #     <style>
# #     .main {
# #         background-color: #f0f2f6;
# #         padding: 20px;
# #         border-radius: 10px;
# #     }
# #     .header {
# #         text-align: center;
# #         color: #2c3e50;
# #         font-size: 2.5em;
# #         margin-bottom: 10px;
# #     }
# #     .subheader {
# #         text-align: center;
# #         color: #7f8c8d;
# #         font-size: 1.2em;
# #         margin-bottom: 20px;
# #     }
# #     .upload-box {
# #         border: 2px dashed #3498db;
# #         padding: 30px;
# #         text-align: center;
# #         background-color: #ffffff;
# #         border-radius: 10px;
# #         margin-bottom: 20px;
# #     }
# #     .upload-text {
# #         color: #3498db;
# #         font-size: 1.1em;
# #     }
# #     .convert-btn {
# #         background-color: #2ecc71;
# #         color: white;
# #         font-weight: bold;
# #         border-radius: 5px;
# #         padding: 10px 20px;
# #     }
# #     .download-link {
# #         color: #e74c3c;
# #         font-weight: bold;
# #     }
# #     .file-info {
# #         background-color: #ecf0f1;
# #         padding: 10px;
# #         border-radius: 5px;
# #         margin-top: 10px;
# #     }
# #     .footer {
# #         text-align: center;
# #         color: #7f8c8d;
# #         margin-top: 20px;
# #         font-size: 0.9em;
# #     }
# #     </style>
# # """, unsafe_allow_html=True)

# # # Streamlit app
# # with st.container():
# #     st.markdown('<h1 class="header">SamDocAI - File Converter</h1>', unsafe_allow_html=True)
# #     st.markdown('<p class="subheader">Transform your multimedia and documents effortlessly into PDF, Word, JPG, or PNG.</p>', unsafe_allow_html=True)

# #     # File uploader
# #     with st.container():
# #         st.markdown('<div class="upload-box"><p class="upload-text">Drag and drop or click to upload a file (up to 1GB)</p></div>', unsafe_allow_html=True)
# #         uploaded_file = st.file_uploader("", type=sum(EXTENSIONS.values(), []), label_visibility="collapsed")

# #     if uploaded_file:
# #         file_ext = get_file_extension(uploaded_file.name)
# #         file_size = bytes_to_size(uploaded_file.size)
# #         st.markdown(f'<div class="file-info">📄 <strong>File:</strong> {uploaded_file.name} ({file_size})</div>', unsafe_allow_html=True)

# #         # Determine available output formats
# #         if file_ext in EXTENSIONS["image"]:
# #             output_options = EXTENSIONS["image"]
# #         elif file_ext in EXTENSIONS["video"]:
# #             output_options = EXTENSIONS["video"] + EXTENSIONS["audio"]
# #         elif file_ext in EXTENSIONS["audio"]:
# #             output_options = EXTENSIONS["audio"]
# #         elif file_ext == "docx":
# #             output_options = ["pdf", "jpg", "png"]
# #         elif file_ext == "pdf":
# #             output_options = ["docx", "jpg", "png", "pdf"]
# #         else:
# #             st.error("Unsupported file type.")
# #             output_options = []

# #         if output_options:
# #             col1, col2 = st.columns([3, 1])
# #             with col1:
# #                 output_format = st.selectbox("Convert to", output_options, index=None, placeholder="Select output format...")
# #             with col2:
# #                 convert_button = st.button("Convert Now", key="convert", help="Start conversion", use_container_width=True, type="primary")

# #             if convert_button and output_format:
# #                 with st.spinner("Converting your file..."):
# #                     result = convert_file(uploaded_file, file_ext, output_format)
                    
# #                     if result:
# #                         st.success("Conversion completed successfully! 🎉")
# #                         if result.suffix in [".zip"]:
# #                             st.info("📦 Multi-page document converted to a ZIP file with images.")
# #                         st.markdown(f'<p class="download-link">{get_binary_file_downloader_html(result, "Download Converted File")}</p>', unsafe_allow_html=True)
# #                         if os.path.exists(result):
# #                             os.remove(result)

# #     # Footer
# import streamlit as st
# import os
# from pathlib import Path
# import ffmpeg
# from PIL import Image
# import io
# import base64
# from PyPDF2 import PdfReader, PdfWriter
# from pdf2docx import Converter as Pdf2DocxConverter
# from docx import Document
# from docx2pdf import convert as docx2pdf_convert
# from pdf2image import convert_from_path
# import zipfile
# import traceback
# import subprocess

# # Set page config as the first Streamlit command
# st.set_page_config(page_title="SamDocAI - File Converter", layout="wide")

# # Force Poppler into PATH (adjust if your Poppler path differs)
# os.environ["PATH"] += os.pathsep + r"C:\poppler-24.08.0\bin"

# # Optionally specify FFmpeg path (uncomment and adjust if needed)
# # FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
# # os.environ["PATH"] += os.pathsep + os.path.dirname(FFMPEG_PATH)

# # Supported file extensions
# EXTENSIONS = {
#     "image": ["jpg", "jpeg", "png", "gif", "bmp", "webp", "ico", "tif", "tiff"],
#     "video": ["mp4", "m4v", "3gp", "avi", "mov", "wmv", "mkv", "flv", "webm"],
#     "audio": ["mp3", "wav", "ogg", "aac", "wma", "flac", "m4a"],
#     "document": ["pdf", "docx"],
# }

# # Utility functions
# def get_file_extension(file_name):
#     return Path(file_name).suffix[1:].lower()

# def remove_file_extension(file_name):
#     return Path(file_name).stem

# def bytes_to_size(bytes_size):
#     sizes = ["Bytes", "KB", "MB", "GB", "TB"]
#     if bytes_size == 0:
#         return "0 Byte"
#     i = min(int((len(str(bytes_size)) - 1) // 3), 4)
#     size = bytes_size / (1024 ** i)
#     return f"{size:.2f} {sizes[i]}"

# def check_ffmpeg():
#     try:
#         subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
#         return True
#     except (subprocess.CalledProcessError, FileNotFoundError):
#         return False

# def convert_file(input_file, input_ext, output_ext):
#     output_base = remove_file_extension(input_file.name)
#     output_filename = f"{output_base}.{output_ext}"
#     output_path = Path(output_filename)

#     try:
#         with open(input_file.name, "wb") as f:
#             f.write(input_file.read())

#         if input_ext in EXTENSIONS["image"] and output_ext in EXTENSIONS["image"]:
#             img = Image.open(input_file.name)
#             save_format = "TIFF" if output_ext in ["tif", "tiff"] else output_ext.upper()
#             if output_ext == "jpg" or output_ext == "jpeg":
#                 if img.mode in ("RGBA", "CMYK"):
#                     img = img.convert("RGB")
#                 img.save(output_path, format="JPEG", quality=95)
#             else:
#                 img.save(output_path, format=save_format)
#         elif input_ext == "mp4" and output_ext == "mp3":
#             if not check_ffmpeg():
#                 raise FileNotFoundError("FFmpeg is not installed or not found in PATH. Please install FFmpeg and add it to your system PATH.")
#             stream = ffmpeg.input(input_file.name)
#             stream = ffmpeg.output(stream, output_filename, acodec="mp3", ab="128k")
#             ffmpeg.run(stream, overwrite_output=True)
#         elif input_ext in EXTENSIONS["audio"] and output_ext in EXTENSIONS["audio"]:
#             if not check_ffmpeg():
#                 raise FileNotFoundError("FFmpeg is not installed or not found in PATH. Please install FFmpeg and add it to your system PATH.")
#             stream = ffmpeg.input(input_file.name)
#             stream = ffmpeg.output(stream, output_filename)
#             ffmpeg.run(stream, overwrite_output=True)
#         elif input_ext == "docx":
#             if output_ext == "pdf":
#                 docx2pdf_convert(input_file.name, output_filename)
#             elif output_ext in ["jpg", "png"]:
#                 temp_pdf = f"{output_base}_temp.pdf"
#                 docx2pdf_convert(input_file.name, temp_pdf)
#                 images = convert_from_path(temp_pdf, dpi=300)
#                 if len(images) == 1:
#                     if output_ext == "jpg":
#                         images[0].save(output_path, format="JPEG", quality=95)
#                     else:
#                         images[0].save(output_path, format="PNG")
#                 else:
#                     zip_filename = f"{output_base}.zip"
#                     with zipfile.ZipFile(zip_filename, 'w') as zipf:
#                         for i, img in enumerate(images):
#                             img_path = f"{output_base}_page_{i+1}.{output_ext}"
#                             if output_ext == "jpg":
#                                 img.save(img_path, format="JPEG", quality=95)
#                             else:
#                                 img.save(img_path, format="PNG")
#                             zipf.write(img_path)
#                             os.remove(img_path)
#                     output_path = Path(zip_filename)
#                 os.remove(temp_pdf)
#         elif input_ext == "pdf":
#             if output_ext == "docx":
#                 cv = Pdf2DocxConverter(input_file.name)
#                 cv.convert(output_filename)
#                 cv.close()
#             elif output_ext in ["jpg", "png"]:
#                 images = convert_from_path(input_file.name, dpi=300)
#                 if len(images) == 1:
#                     if output_ext == "jpg":
#                         images[0].save(output_path, format="JPEG", quality=95)
#                     else:
#                         images[0].save(output_path, format="PNG")
#                 else:
#                     zip_filename = f"{output_base}.zip"
#                     with zipfile.ZipFile(zip_filename, 'w') as zipf:
#                         for i, img in enumerate(images):
#                             img_path = f"{output_base}_page_{i+1}.{output_ext}"
#                             if output_ext == "jpg":
#                                 img.save(img_path, format="JPEG", quality=95)
#                             else:
#                                 img.save(img_path, format="PNG")
#                             zipf.write(img_path)
#                             os.remove(img_path)
#                     output_path = Path(zip_filename)
#             elif output_ext == "pdf":
#                 reader = PdfReader(input_file.name)
#                 writer = PdfWriter()
#                 for page in reader.pages:
#                     writer.add_page(page)
#                 with open(output_filename, "wb") as f:
#                     writer.write(f)
#         else:
#             raise ValueError(f"Conversion from {input_ext} to {output_ext} is not supported. MP4 can only be converted to MP3.")

#         # Read the file content before cleanup
#         with open(output_path, "rb") as f:
#             file_content = f.read()

#         return output_path, file_content
#     except Exception as e:
#         st.error(f"Error converting {input_file.name}: {str(e)}\n\nDetails: {traceback.format_exc()}")
#         return None, None
#     finally:
#         if os.path.exists(input_file.name):
#             os.remove(input_file.name)

# # Custom CSS for light blue theme with enhanced design
# st.markdown("""
#     <style>
#     .main {
#         background-color: #e6f0fa;
#         padding: 20px;
#         border-radius: 10px;
#         border: 1px solid #b3d4fc;
#     }
#     .header {
#         text-align: center;
#         color: #004085;
#         font-size: 2.5em;
#         margin-bottom: 10px;
#         font-family: 'Arial', sans-serif;
#     }
#     .subheader {
#         text-align: center;
#         color: #0056b3;
#         font-size: 1.2em;
#         margin-bottom: 20px;
#         font-family: 'Arial', sans-serif;
#     }
#     .upload-box {
#         border: 2px dashed #007bff;
#         padding: 30px;
#         text-align: center;
#         background-color: #f8fbff;
#         border-radius: 10px;
#         margin-bottom: 20px;
#         box-shadow: 0 2px 4px rgba(0, 123, 255, 0.1);
#     }
#     .upload-text {
#         color: #0056b3;
#         font-size: 1.1em;
#         font-family: 'Arial', sans-serif;
#     }
#     .stButton>button {
#         background-color: #007bff;
#         color: white;
#         font-weight: bold;
#         border-radius: 8px;
#         padding: 12px 24px;
#         border: 1px solid #0056b3;
#         box-shadow: 0 2px 4px rgba(0, 123, 255, 0.2);
#         transition: all 0.3s ease;
#     }
#     .stButton>button:hover {
#         background-color: #0056b3;
#         box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
#     }
#     .file-info {
#         background-color: #f8fbff;
#         padding: 10px;
#         border-radius: 5px;
#         margin-top: 10px;
#         border: 1px solid #b3d4fc;
#         color: #004085;
#     }
#     .footer {
#         text-align: center;
#         color: #0056b3;
#         margin-top: 20px;
#         font-size: 0.9em;
#         font-family: 'Arial', sans-serif;
#     }
#     .stSelectbox > div > div {
#         border: 1px solid #b3d4fc;
#         border-radius: 5px;
#     }
#     .stSpinner > div {
#         color: #007bff;
#     }
#     .stSuccess {
#         background-color: #cce5ff;
#         border: 1px solid #007bff;
#         color: #004085;
#     }
#     .stInfo {
#         background-color: #cce5ff;
#         border: 1px solid #007bff;
#         color: #004085;
#     }
#     .stError {
#         background-color: #ffe6e6;
#         border: 1px solid #dc3545;
#         color: #721c24;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Streamlit app
# with st.container():
#     st.markdown('<h1 class="header">SamDocAI - File Converter</h1>', unsafe_allow_html=True)
#     st.markdown('<p class="subheader">Convert up to 10 files at once. MP4 files can only be converted to MP3.</p>', unsafe_allow_html=True)

#     # File uploader (up to 10 files)
#     with st.container():
#         st.markdown('<div class="upload-box"><p class="upload-text">Drag and drop or click to upload up to 10 files (max 1GB each)</p></div>', unsafe_allow_html=True)
#         uploaded_files = st.file_uploader("", type=sum(EXTENSIONS.values(), []), accept_multiple_files=True, label_visibility="collapsed")

#     if uploaded_files:
#         if len(uploaded_files) > 10:
#             st.error("You can only upload up to 10 files at a time.")
#         else:
#             st.markdown("### Uploaded Files", unsafe_allow_html=True)
#             # Store selected formats in session state
#             if "output_formats" not in st.session_state:
#                 st.session_state.output_formats = {}

#             # Display files and their format selectors
#             for i, uploaded_file in enumerate(uploaded_files):
#                 file_ext = get_file_extension(uploaded_file.name)
#                 file_size = bytes_to_size(uploaded_file.size)
#                 st.markdown(f'<div class="file-info">📄 <strong>File {i+1}:</strong> {uploaded_file.name} ({file_size})</div>', unsafe_allow_html=True)

#                 # Determine available output formats
#                 if file_ext in EXTENSIONS["image"]:
#                     output_options = EXTENSIONS["image"]
#                 elif file_ext == "mp4":
#                     output_options = ["mp3"]  # Only MP3 for MP4
#                 elif file_ext in EXTENSIONS["video"] and file_ext != "mp4":
#                     output_options = EXTENSIONS["video"] + EXTENSIONS["audio"]
#                 elif file_ext in EXTENSIONS["audio"]:
#                     output_options = EXTENSIONS["audio"]
#                 elif file_ext == "docx":
#                     output_options = ["pdf", "jpg", "png"]
#                 elif file_ext == "pdf":
#                     output_options = ["docx", "jpg", "png", "pdf"]
#                 else:
#                     st.error(f"Unsupported file type: {uploaded_file.name}")
#                     output_options = []

#                 if output_options:
#                     # Unique key for each selectbox
#                     key = f"format_{i}_{uploaded_file.name}"
#                     selected_format = st.selectbox(
#                         f"Select output format for {uploaded_file.name}",
#                         output_options,
#                         index=None,
#                         placeholder="Choose format...",
#                         key=key
#                     )
#                     st.session_state.output_formats[uploaded_file.name] = selected_format

#             # Convert button
#             if st.button("Convert All Files", use_container_width=True, type="primary"):
#                 with st.spinner("Converting your files..."):
#                     results = []
#                     for uploaded_file in uploaded_files:
#                         output_format = st.session_state.output_formats.get(uploaded_file.name)
#                         if output_format:
#                             file_ext = get_file_extension(uploaded_file.name)
#                             result_path, result_content = convert_file(uploaded_file, file_ext, output_format)
#                             if result_path and result_content:
#                                 results.append((uploaded_file.name, result_path, result_content))
#                             else:
#                                 st.error(f"Failed to convert {uploaded_file.name}.")
#                         else:
#                             st.warning(f"No output format selected for {uploaded_file.name}. Skipping conversion.")

#                     if results:
#                         st.success("Conversion completed successfully! 🎉")
#                         for original_name, result_path, result_content in results:
#                             if result_path.suffix in [".zip"]:
#                                 st.info(f"📦 {original_name} converted to a ZIP file with images.")
#                             st.download_button(
#                                 label=f"Download {result_path.name}",
#                                 data=result_content,
#                                 file_name=result_path.name,
#                                 mime="application/octet-stream",
#                                 key=f"download_{original_name}"
#                             )
#                             # Clean up after download
#                             if os.path.exists(result_path):
#                                 os.remove(result_path)

import streamlit as st
import os
from pathlib import Path
import ffmpeg
from PIL import Image
import io
import base64
from PyPDF2 import PdfReader, PdfWriter
from pdf2docx import Converter as Pdf2DocxConverter
from docx import Document
from docx2pdf import convert as docx2pdf_convert
from pdf2image import convert_from_path
import zipfile
import traceback
import subprocess

# Set page config as the first Streamlit command
st.set_page_config(page_title="SamDocAI - File Converter", layout="wide")

# Force Poppler into PATH (adjust if your Poppler path differs)
os.environ["PATH"] += os.pathsep + r"C:\poppler-24.08.0\bin"

# Optionally specify FFmpeg path (uncomment and adjust if needed)
# FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
# os.environ["PATH"] += os.pathsep + os.path.dirname(FFMPEG_PATH)

# Supported file extensions
EXTENSIONS = {
    "image": ["jpg", "jpeg", "png", "gif", "bmp", "webp", "ico", "tif", "tiff"],
    "video": ["mp4", "m4v", "3gp", "avi", "mov", "wmv", "mkv", "flv", "webm"],
    "audio": ["wav", "ogg", "aac", "wma", "flac", "m4a"],  # Removed "mp3" from uploadable types
    "document": ["pdf", "docx"],
}

# Utility functions
def get_file_extension(file_name):
    return Path(file_name).suffix[1:].lower()

def remove_file_extension(file_name):
    return Path(file_name).stem

def bytes_to_size(bytes_size):
    sizes = ["Bytes", "KB", "MB", "GB", "TB"]
    if bytes_size == 0:
        return "0 Byte"
    i = min(int((len(str(bytes_size)) - 1) // 3), 4)
    size = bytes_size / (1024 ** i)
    return f"{size:.2f} {sizes[i]}"

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def convert_file(input_file, input_ext, output_ext):
    output_base = remove_file_extension(input_file.name)
    output_filename = f"{output_base}.{output_ext}"
    output_path = Path(output_filename)

    try:
        with open(input_file.name, "wb") as f:
            f.write(input_file.read())

        if input_ext in EXTENSIONS["image"]:
            img = Image.open(input_file.name)
            if output_ext in EXTENSIONS["image"]:
                save_format = "TIFF" if output_ext in ["tif", "tiff"] else output_ext.upper()
                if output_ext == "jpg" or output_ext == "jpeg":
                    if img.mode in ("RGBA", "CMYK"):
                        img = img.convert("RGB")
                    img.save(output_path, format="JPEG", quality=95)
                else:
                    img.save(output_path, format=save_format)
            elif output_ext == "pdf":
                if img.mode == "RGBA":
                    img = img.convert("RGB")
                img.save(output_path, format="PDF")
            elif output_ext == "docx":
                doc = Document()
                doc.add_picture(input_file.name)
                doc.save(output_path)
        elif input_ext == "mp4" and output_ext == "mp3":
            if not check_ffmpeg():
                raise FileNotFoundError("FFmpeg is not installed or not found in PATH. Please install FFmpeg and add it to your system PATH.")
            stream = ffmpeg.input(input_file.name)
            stream = ffmpeg.output(stream, output_filename, acodec="mp3", ab="128k")
            ffmpeg.run(stream, overwrite_output=True)
        elif input_ext in EXTENSIONS["audio"] and output_ext in EXTENSIONS["audio"]:
            if not check_ffmpeg():
                raise FileNotFoundError("FFmpeg is not installed or not found in PATH. Please install FFmpeg and add it to your system PATH.")
            stream = ffmpeg.input(input_file.name)
            stream = ffmpeg.output(stream, output_filename)
            ffmpeg.run(stream, overwrite_output=True)
        elif input_ext == "docx":
            if output_ext == "pdf":
                docx2pdf_convert(input_file.name, output_filename)
            elif output_ext in ["jpg", "png"]:
                temp_pdf = f"{output_base}_temp.pdf"
                docx2pdf_convert(input_file.name, temp_pdf)
                images = convert_from_path(temp_pdf, dpi=300)
                if len(images) == 1:
                    if output_ext == "jpg":
                        images[0].save(output_path, format="JPEG", quality=95)
                    else:
                        images[0].save(output_path, format="PNG")
                else:
                    zip_filename = f"{output_base}.zip"
                    with zipfile.ZipFile(zip_filename, 'w') as zipf:
                        for i, img in enumerate(images):
                            img_path = f"{output_base}_page_{i+1}.{output_ext}"
                            if output_ext == "jpg":
                                img.save(img_path, format="JPEG", quality=95)
                            else:
                                img.save(img_path, format="PNG")
                            zipf.write(img_path)
                            os.remove(img_path)
                    output_path = Path(zip_filename)
                os.remove(temp_pdf)
        elif input_ext == "pdf":
            if output_ext == "docx":
                cv = Pdf2DocxConverter(input_file.name)
                cv.convert(output_filename)
                cv.close()
            elif output_ext in ["jpg", "png"]:
                images = convert_from_path(input_file.name, dpi=300)
                if len(images) == 1:
                    if output_ext == "jpg":
                        images[0].save(output_path, format="JPEG", quality=95)
                    else:
                        images[0].save(output_path, format="PNG")
                else:
                    zip_filename = f"{output_base}.zip"
                    with zipfile.ZipFile(zip_filename, 'w') as zipf:
                        for i, img in enumerate(images):
                            img_path = f"{output_base}_page_{i+1}.{output_ext}"
                            if output_ext == "jpg":
                                img.save(img_path, format="JPEG", quality=95)
                            else:
                                img.save(img_path, format="PNG")
                            zipf.write(img_path)
                            os.remove(img_path)
                    output_path = Path(zip_filename)
            elif output_ext == "pdf":
                reader = PdfReader(input_file.name)
                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)
                with open(output_filename, "wb") as f:
                    writer.write(f)
        else:
            raise ValueError(f"Conversion from {input_ext} to {output_ext} is not supported. MP4 can only be converted to MP3.")

        # Read the file content before cleanup
        with open(output_path, "rb") as f:
            file_content = f.read()

        return output_path, file_content
    except Exception as e:
        st.error(f"Error converting {input_file.name}: {str(e)}\n\nDetails: {traceback.format_exc()}")
        return None, None
    finally:
        if os.path.exists(input_file.name):
            os.remove(input_file.name)

# Custom CSS for light blue theme with enhanced design
st.markdown("""
    <style>
    .main {
        background-color: #e6f0fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #b3d4fc;
    }
    .header {
        text-align: center;
        color: #004085;
        font-size: 2.5em;
        margin-bottom: 10px;
        font-family: 'Arial', sans-serif;
    }
    .subheader {
        text-align: center;
        color: #0056b3;
        font-size: 1.2em;
        margin-bottom: 20px;
        font-family: 'Arial', sans-serif;
    }
    .upload-box {
        border: 2px dashed #007bff;
        padding: 30px;
        text-align: center;
        background-color: #f8fbff;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0, 123, 255, 0.1);
    }
    .upload-text {
        color: #0056b3;
        font-size: 1.1em;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px 24px;
        border: 1px solid #0056b3;
        box-shadow: 0 2px 4px rgba(0, 123, 255, 0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        box-shadow: 0 4px 8px rgba(0, 123, 255, 0.3);
    }
    .file-info {
        background-color: #f8fbff;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
        border: 1px solid #b3d4fc;
        color: #004085;
    }
    .footer {
        text-align: center;
        color: #0056b3;
        margin-top: 20px;
        font-size: 0.9em;
        font-family: 'Arial', sans-serif;
    }
    .stSelectbox > div > div {
        border: 1px solid #b3d4fc;
        border-radius: 5px;
    }
    .stSpinner > div {
        color: #007bff;
    }
    .stSuccess {
        background-color: #cce5ff;
        border: 1px solid #007bff;
        color: #004085;
    }
    .stInfo {
        background-color: #cce5ff;
        border: 1px solid #007bff;
        color: #004085;
    }
    .stError {
        background-color: #ffe6e6;
        border: 1px solid #dc3545;
        color: #721c24;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit app
with st.container():
    st.markdown('<h1 class="header">SamDocAI - File Converter</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">Convert up to 10 files at once. MP4 files can only be converted to MP3. Images can also be converted to PDF and Word.</p>', unsafe_allow_html=True)

    # File uploader (up to 10 files, excluding MP3)
    with st.container():
        st.markdown('<div class="upload-box"><p class="upload-text">Drag and drop or click to upload up to 10 files (max 1GB each, no MP3)</p></div>', unsafe_allow_html=True)
        # Exclude "mp3" from the allowed types
        allowed_types = EXTENSIONS["image"] + EXTENSIONS["video"] + EXTENSIONS["audio"] + EXTENSIONS["document"]
        uploaded_files = st.file_uploader("", type=allowed_types, accept_multiple_files=True, label_visibility="collapsed")

    if uploaded_files:
        if len(uploaded_files) > 10:
            st.error("You can only upload up to 10 files at a time.")
        else:
            st.markdown("### Uploaded Files", unsafe_allow_html=True)
            # Store selected formats in session state
            if "output_formats" not in st.session_state:
                st.session_state.output_formats = {}

            # Display files and their format selectors
            for i, uploaded_file in enumerate(uploaded_files):
                file_ext = get_file_extension(uploaded_file.name)
                file_size = bytes_to_size(uploaded_file.size)
                st.markdown(f'<div class="file-info">📄 <strong>File {i+1}:</strong> {uploaded_file.name} ({file_size})</div>', unsafe_allow_html=True)

                # Determine available output formats
                if file_ext in EXTENSIONS["image"]:
                    output_options = EXTENSIONS["image"] + ["pdf", "docx"]
                elif file_ext == "mp4":
                    output_options = ["mp3"]  # Only MP3 for MP4
                elif file_ext in EXTENSIONS["video"] and file_ext != "mp4":
                    output_options = EXTENSIONS["video"] + EXTENSIONS["audio"]
                elif file_ext in EXTENSIONS["audio"]:
                    output_options = EXTENSIONS["audio"]
                elif file_ext == "docx":
                    output_options = ["pdf", "jpg", "png"]
                elif file_ext == "pdf":
                    output_options = ["docx", "jpg", "png", "pdf"]
                else:
                    st.error(f"Unsupported file type: {uploaded_file.name}")
                    output_options = []

                if output_options:
                    # Unique key for each selectbox
                    key = f"format_{i}_{uploaded_file.name}"
                    selected_format = st.selectbox(
                        f"Select output format for {uploaded_file.name}",
                        output_options,
                        index=None,
                        placeholder="Choose format...",
                        key=key
                    )
                    st.session_state.output_formats[uploaded_file.name] = selected_format

            # Convert button
            if st.button("Convert All Files", use_container_width=True, type="primary"):
                with st.spinner("Converting your files..."):
                    results = []
                    for uploaded_file in uploaded_files:
                        output_format = st.session_state.output_formats.get(uploaded_file.name)
                        if output_format:
                            file_ext = get_file_extension(uploaded_file.name)
                            result_path, result_content = convert_file(uploaded_file, file_ext, output_format)
                            if result_path and result_content:
                                results.append((uploaded_file.name, result_path, result_content))
                            else:
                                st.error(f"Failed to convert {uploaded_file.name}.")
                        else:
                            st.warning(f"No output format selected for {uploaded_file.name}. Skipping conversion.")

                    if results:
                        st.success("Conversion completed successfully! 🎉")
                        for original_name, result_path, result_content in results:
                            if result_path.suffix in [".zip"]:
                                st.info(f"📦 {original_name} converted to a ZIP file with images.")
                            st.download_button(
                                label=f"Download {result_path.name}",
                                data=result_content,
                                file_name=result_path.name,
                                mime="application/octet-stream",
                                key=f"download_{original_name}"
                            )
                            # Clean up after download
                            if os.path.exists(result_path):
                                os.remove(result_path)

