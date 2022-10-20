poster:
	pandoc poster.md -o poster.html -c styles.css --standalone

report:
	pandoc report.md -o report.pdf
