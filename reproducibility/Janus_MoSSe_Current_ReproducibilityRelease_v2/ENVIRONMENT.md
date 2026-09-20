# Numerical environment used for the audit-resolved calculations

- Python: 3.13.5
- Platform: Linux x86_64, glibc 2.41
- numpy: 2.3.5
- pandas: 2.2.3
- scipy: 1.17.0
- numba: 0.65.1
- matplotlib: 3.10.8
- python-docx: 1.2.0 (manuscript generation/layout only)

The pinned numerical dependencies in `requirements.txt` reproduce the scientific Python stack used by the inherited material engine and the audit-resolution scripts. Numerical validation should be run with `python validate_release.py` after installation.
