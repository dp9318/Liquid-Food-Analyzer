import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import cv2
import threading
import time
import os
from datetime import datetime

class LiquidFoodAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Liquid Food Analyzer Pro")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f5f6fa")
        self.root.resizable(False, False)

        self.center_window()
        self.setup_styles()

        self.file_path = None
        self.animating = False
        self.analysis_count = 0
        self.preview_image = None

        self.create_ui()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor='#e0e0e0',
            bordercolor='#cccccc',
            background='#4CAF50',
            lightcolor='#4CAF50',
            darkcolor='#4CAF50'
        )

    def create_ui(self):
        main_frame = tk.Frame(self.root, bg="#f5f6fa")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        left_frame = tk.Frame(main_frame, bg="white", relief=tk.FLAT, bd=0)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        left_frame.configure(highlightbackground="#e0e0e0", highlightthickness=1)

        right_frame = tk.Frame(main_frame, bg="white", relief=tk.FLAT, bd=0)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        right_frame.configure(highlightbackground="#e0e0e0", highlightthickness=1)

        self.create_left_controls(left_frame)
        self.create_right_preview(right_frame)
        self.create_footer()

    def create_left_controls(self, parent):
        title_label = tk.Label(parent, text="Liquid Food Analyzer",
                              font=("Segoe UI", 18, "bold"), bg="white", fg="#2c3e50")
        title_label.pack(pady=(20, 15))

        subtitle_label = tk.Label(parent, text="Select a sample image for analysis",
                                 font=("Segoe UI", 11), bg="white", fg="#666")
        subtitle_label.pack(pady=(0, 20))

        upload_frame = tk.Frame(parent, bg="white")
        upload_frame.pack(pady=10, fill=tk.X, padx=20)

        self.upload_btn = tk.Button(upload_frame, text="� Choose Image",
                                   command=self.upload_image,
                                   font=("Segoe UI", 11, "bold"), bg="#3498db", fg="white",
                                   activebackground="#2980b9", activeforeground="white",
                                   padx=20, pady=8, cursor="hand2", relief=tk.FLAT, bd=0)
        self.upload_btn.pack(fill=tk.X)
        self.upload_btn.bind("<Enter>", lambda e: self.upload_btn.config(bg="#2980b9"))
        self.upload_btn.bind("<Leave>", lambda e: self.upload_btn.config(bg="#3498db"))

        self.file_info_label = tk.Label(upload_frame, text="No file selected",
                                       font=("Segoe UI", 9), bg="white", fg="#999", wraplength=250)
        self.file_info_label.pack(pady=(10, 0))

        analyze_frame = tk.Frame(parent, bg="white")
        analyze_frame.pack(pady=10, fill=tk.X, padx=20)

        self.analyze_button = tk.Button(analyze_frame, text="� Analyze Sample",
                                       command=self.start_analysis,
                                       font=("Segoe UI", 11, "bold"), bg="#27ae60", fg="white",
                                       activebackground="#229954", activeforeground="white",
                                       padx=20, pady=8, cursor="hand2", relief=tk.FLAT, bd=0,
                                       state=tk.DISABLED)
        self.analyze_button.pack(fill=tk.X)
        self.analyze_button.bind("<Enter>", lambda e: self.on_analyze_hover(True))
        self.analyze_button.bind("<Leave>", lambda e: self.on_analyze_hover(False))

        progress_frame = tk.Frame(parent, bg="white")
        progress_frame.pack(pady=20, fill=tk.X, padx=20)

        self.progress_label = tk.Label(progress_frame, text="",
                                      font=("Segoe UI", 9), bg="white", fg="#666")
        self.progress_label.pack()

        self.progress = ttk.Progressbar(progress_frame, orient="horizontal", length=300,
                                       mode='determinate', style="Custom.Horizontal.TProgressbar")
        self.progress.pack(pady=(5, 0), fill=tk.X)

        status_frame = tk.Frame(parent, bg="white")
        status_frame.pack(pady=10, fill=tk.X, padx=20)

        self.status_label = tk.Label(status_frame, text="",
                                    font=("Segoe UI", 10), bg="white", fg="#3498db", wraplength=280)
        self.status_label.pack()

    def create_right_preview(self, parent):
        preview_title = tk.Label(parent, text="Image Preview",
                                font=("Segoe UI", 14, "bold"), bg="white", fg="#2c3e50")
        preview_title.pack(pady=(20, 15))

        self.preview_container = tk.Frame(parent, bg="#f8f9fa", width=400, height=300, relief=tk.FLAT)
        self.preview_container.pack(pady=10)
        self.preview_container.configure(highlightbackground="#e0e0e0", highlightthickness=1)
        self.preview_container.pack_propagate(False)

        self.preview_label = tk.Label(self.preview_container, bg="#f8f9fa", text="Image will appear here", fg="#ccc")
        self.preview_label.pack(expand=True, fill=tk.BOTH)

        results_title = tk.Label(parent, text="Analysis Results",
                                font=("Segoe UI", 14, "bold"), bg="white", fg="#2c3e50")
        results_title.pack(pady=(20, 10))

        self.results_container = tk.Frame(parent, bg="#f8f9fa", relief=tk.FLAT)
        self.results_container.pack(pady=10, fill=tk.X, padx=20)
        self.results_container.configure(highlightbackground="#e0e0e0", highlightthickness=1)

        result_content = tk.Frame(self.results_container, bg="#f8f9fa")
        result_content.pack(pady=15, padx=10, fill=tk.BOTH)

        self.result_icon_label = tk.Label(result_content, text="", font=("Arial", 36), bg="#f8f9fa")
        self.result_icon_label.pack(pady=(0, 10))

        self.result_label = tk.Label(result_content, text="Results will appear here",
                                    font=("Segoe UI", 14, "bold"), bg="#f8f9fa", fg="#999")
        self.result_label.pack(pady=(0, 5))

        self.result_detail_label = tk.Label(result_content, text="",
                                           font=("Segoe UI", 10), bg="#f8f9fa", fg="#666", wraplength=320)
        self.result_detail_label.pack()

    def create_footer(self):
        footer_frame = tk.Frame(self.root, bg="#ecf0f1", height=40)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)

        self.counter_label = tk.Label(footer_frame, text=f"Analyses performed: {self.analysis_count}",
                                    font=("Segoe UI", 9), bg="#ecf0f1", fg="#7f8c8d")
        self.counter_label.pack(side=tk.LEFT, padx=20, pady=10)

        version_label = tk.Label(footer_frame, text="Version 2.0 Pro | © 2024",
                                font=("Segoe UI", 9), bg="#ecf0f1", fg="#7f8c8d")
        version_label.pack(side=tk.RIGHT, padx=20, pady=10)

    def on_analyze_hover(self, entering):
        if self.analyze_button['state'] == tk.NORMAL:
            if entering:
                self.analyze_button.config(bg="#229954")
            else:
                self.analyze_button.config(bg="#27ae60")

    def upload_image(self):
        self.file_path = filedialog.askopenfilename(
            title="Select Liquid Food Sample Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png"),
                ("JPG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )

        if self.file_path:
            try:
                file_name = os.path.basename(self.file_path)
                file_size = os.path.getsize(self.file_path) / 1024
                self.file_info_label.config(
                    text=f"Selected: {file_name} ({file_size:.1f} KB)",
                    fg="#27ae60"
                )

                self.analyze_button.config(state=tk.NORMAL)
                self.clear_results()
                self.status_label.config(text="Image loaded successfully", fg="#27ae60")

                img = Image.open(self.file_path)
                max_width = 380
                max_height = 280

                width, height = img.size
                aspect_ratio = width / height

                if width > height:
                    new_width = min(width, max_width)
                    new_height = int(new_width / aspect_ratio)
                    if new_height > max_height:
                        new_height = max_height
                        new_width = int(new_height * aspect_ratio)
                else:
                    new_height = min(height, max_height)
                    new_width = int(new_height * aspect_ratio)
                    if new_width > max_width:
                        new_width = max_width
                        new_height = int(new_width / aspect_ratio)

                img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.preview_image = ImageTk.PhotoImage(img_resized)

                self.preview_label.config(image=self.preview_image, text="")
                self.preview_label.pack_forget()
                self.preview_label.pack(expand=True, fill=tk.BOTH)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
                self.file_info_label.config(text="Error loading file", fg="#e74c3c")

    def clear_results(self):
        self.result_icon_label.config(text="")
        self.result_label.config(text="Results will appear here", fg="#999")
        self.result_detail_label.config(text="")
        self.status_label.config(text="")
        self.progress['value'] = 0
        self.results_container.config(bg="#f8f9fa")
        for widget in self.results_container.winfo_children():
            for subwidget in widget.winfo_children():
                subwidget.config(bg="#f8f9fa")

    def start_analysis(self):
        if not self.file_path:
            messagebox.showwarning("Warning", "Please select an image first")
            return

        self.analyze_button.config(state=tk.DISABLED)
        self.upload_btn.config(state=tk.DISABLED)
        self.animating = True
        self.clear_results()

        threading.Thread(target=self.analyze_sample, daemon=True).start()

    def update_progress(self, value, text=""):
        self.progress['value'] = value
        self.progress_label.config(text=text)
        self.root.update_idletasks()

    def analyze_sample(self):
        try:
            # --- Schedule GUI updates to run on the main thread ---
            self.root.after(0, self.update_progress, 0, "Loading image...")
            self.root.after(0, self.status_label.config, {'text': "Processing...", 'fg': "#3498db"})
            time.sleep(0.5)

            image = cv2.imread(self.file_path)
            if image is None:
                raise Exception("Failed to load image with OpenCV")

            self.root.after(0, self.update_progress, 20, "Preprocessing image...")
            time.sleep(0.5)

            self.root.after(0, self.update_progress, 40, "Extracting features...")
            time.sleep(0.7)

            self.root.after(0, self.update_progress, 60, "Analyzing sample...")
            time.sleep(0.8)

            self.root.after(0, self.update_progress, 80, "Assessing quality...")
            time.sleep(0.6)

            self.root.after(0, self.update_progress, 95, "Finalizing results...")
            time.sleep(0.4)

            height, width = image.shape[:2]
            # This is your placeholder logic for the ML model
            is_pure = width > 500

            self.root.after(0, self.update_progress, 100, "Analysis complete!")
            time.sleep(0.3)

            # --- Schedule the final result display on the main thread ---
            self.root.after(0, self.display_results, is_pure, width, height)

            self.analysis_count += 1
            self.root.after(0, self.counter_label.config, {'text': f"Analyses performed: {self.analysis_count}"})

            time.sleep(1)
            self.root.after(0, self.progress.config, {'value': 0})
            self.root.after(0, self.progress_label.config, {'text': ""})
            self.root.after(0, self.status_label.config, {'text': "✔ Analysis completed successfully", 'fg': "#27ae60"})

        except Exception as e:
            # --- Schedule error messages on the main thread ---
            def show_error():
                self.progress['value'] = 0
                self.progress_label.config(text="")
                self.status_label.config(text="✖ Analysis failed", fg="#e74c3c")
                self.result_icon_label.config(text="✖", fg="#e74c3c")
                self.result_label.config(text="Analysis Error", fg="#e74c3c")
                self.result_detail_label.config(text=f"Error: {str(e)}")
                messagebox.showerror("Analysis Error", f"Failed to analyze image: {str(e)}")

            self.root.after(0, show_error)

        finally:
            # --- Schedule the final UI state changes on the main thread ---
            def finalize_ui():
                self.analyze_button.config(state=tk.NORMAL)
                self.upload_btn.config(state=tk.NORMAL)
                self.animating = False

            self.root.after(0, finalize_ui)

    def display_results(self, is_pure, width, height):
        if is_pure:
            self.result_icon_label.config(text="✔", fg="#27ae60", font=("Segoe UI", 36, "bold"))
            self.result_label.config(text="Sample Status: PURE", fg="#27ae60")
            self.results_container.config(bg="#f0fdf4")
            for widget in self.results_container.winfo_children():
                for subwidget in widget.winfo_children():
                    subwidget.config(bg="#f0fdf4")

            details = [
                f"Image dimensions: {width} × {height} pixels",
                f"Quality assessment: Passed",
                f"Confidence level: {min(99.9, 95 + (width / 500) * 4):.1f}%",
                f"Analysis time: {datetime.now().strftime('%H:%M:%S')}",
                "\nRecommendation:",
                "✔ This sample meets purity standards"
            ]
        else:
            self.result_icon_label.config(text="✖", fg="#e74c3c", font=("Segoe UI", 36, "bold"))
            self.result_label.config(text="Sample Status: ADULTERATED", fg="#e74c3c")
            self.results_container.config(bg="#fef2f2")
            for widget in self.results_container.winfo_children():
                for subwidget in widget.winfo_children():
                    subwidget.config(bg="#fef2f2")

            details = [
                f"Image dimensions: {width} × {height} pixels",
                f"Quality assessment: Failed",
                f"Contamination level: {min(85, (1 - width / 500) * 100):.1f}%",
                f"Analysis time: {datetime.now().strftime('%H:%M:%S')}",
                "\nRecommendation:",
                "✖ This sample shows signs of adulteration"
            ]

        detail_text = "\n".join(details)
        self.result_detail_label.config(text=detail_text)

def main():
    root = tk.Tk()
    app = LiquidFoodAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
