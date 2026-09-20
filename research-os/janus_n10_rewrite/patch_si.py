from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT

p='/mnt/data/janus_n10_rewrite/Janus_MoSSe_ClaimFrozen_SI_v1.docx'
d=Document(p)

def set_cell(cell,text,fs=8):
    cell.text=str(text)
    cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
    for p in cell.paragraphs:
        p.paragraph_format.space_after=Pt(0)
        for r in p.runs: r.font.size=Pt(fs)

# locate tables by first header
byhead={t.rows[0].cells[0].text.strip():t for t in d.tables}
# update linear table
S9=byhead['Case / theta']
vals={
'Rigid, 1.5 deg':['3.071135','1.258672','0.418601','0'],
'Elastic C, 1.5 deg':['2.934302','1.190210','0.422860','0.459%'],
'Elastic C/2, 1.5 deg':['2.807397','1.135229','0.424125','0.824%'],
'Elastic 2C, 1.5 deg':['3.001636','1.222534','0.421172','0.244%'],
'Elastic C, 3 deg':['1.573022','0.631274','0.427233','0.864%'],
'Elastic C/2, 3 deg':['1.244897','0.516821','0.413276','1.597%'],
'Rigid-limit 100C, 1.5 deg':['3.069751','1.257886','0.418673','0.0052%'],
}
for row in S9.rows[1:]:
    k=row.cells[0].text.strip()
    if k in vals:
        for j,v in enumerate(vals[k],1): set_cell(row.cells[j],v,8)
# nonlinear table
S10=byhead['case']
vals2={
'theta=1.5, C/2':['2.810107','1.135693','0.424353','+0.0966%','+0.0390%','positive'],
'theta=1.5, C':['2.935400','1.190479','0.422921','+0.0374%','+0.0226%','positive'],
'theta=3.0, C':['1.574365','0.631006','0.427755','+0.0854%','-0.0425%','positive'],
}
for row in S10.rows[1:]:
    k=row.cells[0].text.strip()
    if k in vals2:
        for j,v in enumerate(vals2[k],1): set_cell(row.cells[j],v,8)

# Move S8b caption+table to after S8a table.
t8b=byhead['T*']  # ambiguous dict last wins => this is S8a, so find explicitly by second header
for t in d.tables:
    hdr=[c.text.strip() for c in t.rows[0].cells]
    if hdr[:2]==['T*','mean u']:
        joint=t
    if hdr[:2]==['T*','mean v']:
        comp=t
# locate caption para
cap=None
for para in d.paragraphs:
    if para.text.strip().startswith('Table S8b.'):
        cap=para; break
if cap is not None:
    # detach caption and joint table from current position
    cap_el=cap._p
    tbl_el=joint._tbl
    parent=cap_el.getparent(); parent.remove(cap_el)
    parent2=tbl_el.getparent(); parent2.remove(tbl_el)
    # insert after component table: comp -> caption -> joint table
    comp._tbl.addnext(cap_el)
    cap_el.addnext(tbl_el)

d.save(p)
