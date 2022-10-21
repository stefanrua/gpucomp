poster:
	pandoc poster.md -o poster.html -c styles.css --standalone
	cp poster.html acat2022.html

report:
	pandoc report.md -o report.pdf
