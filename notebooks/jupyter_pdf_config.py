# Jupyter nbconvert configuration for PDF export
# Usage: jupyter nbconvert --to pdf --config jupyter_pdf_config.py your_notebook.ipynb

c = get_config()

# Hide code cells, show only outputs
c.TemplateExporter.exclude_input = True

# Don't exclude any output
c.TemplateExporter.exclude_output = False

# Don't exclude output with prompts
c.TemplateExporter.exclude_output_prompt = True

# Don't exclude markdown cells
c.TemplateExporter.exclude_markdown = False

# Don't exclude raw cells
c.TemplateExporter.exclude_raw = False

# Set max output length to unlimited (or very large number)
c.TemplateExporter.max_output_length = -1  # -1 means no limit

# For LaTeX/PDF specific settings
c.PDFExporter.exclude_input = True
c.PDFExporter.template_file = 'article'  # Use article template

# Preprocessor settings to show all output
c.Preprocessor.enabled = True
