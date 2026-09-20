import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Ellipse
from matplotlib.collections import LineCollection
from pathlib import Path

out=Path(__file__).resolve().parent
# 9.0 cm x 4.0 cm exactly
fig=plt.figure(figsize=(9/2.54,4/2.54), dpi=600, facecolor='white')
ax=fig.add_axes([0,0,1,1])
ax.set_xlim(0,9); ax.set_ylim(0,4); ax.axis('off')

# Palette: color-vision friendly and restrained
blue='#2E86AB'; orange='#E67E22'; dark='#37474F'; green='#2E7D32'; light='#ECEFF1'; purple='#7E57C2'

# LEFT: author-original schematic Janus finite contact
# bottom triangular lattice
pts=[]
for j in range(4):
    for i in range(5):
        x=0.55 + i*0.42 + (j%2)*0.21
        y=0.75 + j*0.36
        pts.append((x,y))
for x,y in pts:
    ax.add_patch(Circle((x,y),0.105,facecolor=orange,edgecolor='white',lw=0.35,zorder=2))
    ax.add_patch(Circle((x,y+0.11),0.075,facecolor=dark,edgecolor='white',lw=0.3,zorder=3))
# top finite patch, slightly rotated/offset
th=np.deg2rad(10)
ctr=np.array([1.45,2.65])
top=[]
for j in range(4):
    for i in range(5):
        p=np.array([0.55 + i*0.42 + (j%2)*0.21, 2.05 + j*0.36])
        q=ctr + np.array([[np.cos(th),-np.sin(th)],[np.sin(th),np.cos(th)]])@(p-ctr)
        top.append(q)
for x,y in top:
    if 0.35<x<2.65 and 1.9<y<3.75:
        ax.add_patch(Circle((x,y),0.105,facecolor=blue,edgecolor='white',lw=0.35,zorder=4))
        ax.add_patch(Circle((x,y-0.11),0.075,facecolor=dark,edgecolor='white',lw=0.3,zorder=5))
# subtle finite-contact outline
hexang=np.linspace(0,2*np.pi,7)+np.pi/6
hx=1.55+1.05*np.cos(hexang); hy=2.75+0.72*np.sin(hexang)
ax.plot(hx,hy,color=dark,lw=0.8,zorder=6)

# Transition arrow to registry landscape
ax.add_patch(FancyArrowPatch((2.65,2.0),(3.25,2.0),arrowstyle='-|>',mutation_scale=9,lw=0.9,color=dark))

# CENTER: asymmetric registry-energy landscape (illustrative, not a plotted result)
x=np.linspace(3.1,5.75,160); y=np.linspace(0.45,3.55,150)
X,Y=np.meshgrid(x,y)
# deliberately asymmetric but smooth periodic-like field
Z=(0.55*np.cos(2.7*(X-3.1))+0.34*np.cos(2.15*(Y-0.45)+0.7)+0.22*np.sin(2.1*(X+0.65*Y))
   +0.13*np.sin(4.0*(X-0.3*Y)+0.8))
levels=np.linspace(Z.min(),Z.max(),11)
ax.contourf(X,Y,Z,levels=levels,cmap='PuBu',alpha=0.82,antialiased=True)
ax.contour(X,Y,Z,levels=levels[::2],colors='white',linewidths=0.32,alpha=0.65)
# prepared state marker and opposite load arrows of equal visual weight
minidx=np.unravel_index(np.argmin(Z),Z.shape)
px,py=X[minidx],Y[minidx]
ax.add_patch(Circle((px,py),0.11,facecolor='white',edgecolor=dark,lw=0.7,zorder=9))
ax.add_patch(FancyArrowPatch((px,py+0.16),(px,py+0.86),arrowstyle='-|>',mutation_scale=9,lw=1.0,color=dark,zorder=10))
ax.add_patch(FancyArrowPatch((px,py-0.16),(px,py-0.58),arrowstyle='-|>',mutation_scale=9,lw=1.0,color=dark,zorder=10))
# asymmetry cue: unequal barrier arcs
ax.add_patch(Ellipse((px+0.28,py+0.44),0.42,0.22,angle=20,fill=False,edgecolor=purple,lw=1.1,zorder=11))
ax.add_patch(Ellipse((px-0.18,py-0.34),0.25,0.14,angle=-20,fill=False,edgecolor=purple,lw=0.75,zorder=11))

# Transition arrow to vector transport
ax.add_patch(FancyArrowPatch((5.9,2.0),(6.35,2.0),arrowstyle='-|>',mutation_scale=9,lw=0.9,color=dark))

# RIGHT: lattice-vector relative-periodic transport under zero-mean rocking
# triangular lattice background
for j in range(7):
    for i in range(6):
        xx=6.45+i*0.38+(j%2)*0.19
        yy=0.62+j*0.38
        if xx<8.75:
            ax.add_patch(Circle((xx,yy),0.032,facecolor='#B0BEC5',edgecolor='none',zorder=1))
# oscillatory drive cue (double-headed arrow)
ax.add_patch(FancyArrowPatch((6.45,3.45),(7.55,3.45),arrowstyle='<->',mutation_scale=8,lw=0.8,color=dark,zorder=6))
# repeated-cycle path with net oblique winding
path=np.array([[6.55,0.85],[6.92,1.25],[6.66,1.62],[7.06,2.00],[6.86,2.35],[7.28,2.72],[7.08,3.02],[7.55,3.28]])
segs=np.stack([path[:-1],path[1:]],axis=1)
ax.add_collection(LineCollection(segs,colors=green,linewidths=1.5,zorder=7))
for x0,y0 in path[:-1]:
    ax.add_patch(Circle((x0,y0),0.065,facecolor='white',edgecolor=green,lw=0.75,zorder=8))
ax.add_patch(FancyArrowPatch(tuple(path[-2]),tuple(path[-1]),arrowstyle='-|>',mutation_scale=11,lw=1.5,color=green,zorder=9))
# faint vector basis arrows for lattice displacement
ax.add_patch(FancyArrowPatch((8.0,0.65),(8.6,0.65),arrowstyle='-|>',mutation_scale=7,lw=0.65,color=dark,alpha=0.75))
ax.add_patch(FancyArrowPatch((8.0,0.65),(8.32,1.18),arrowstyle='-|>',mutation_scale=7,lw=0.65,color=dark,alpha=0.75))

# light bounding flow accent
ax.add_patch(FancyArrowPatch((0.25,0.25),(8.75,0.25),arrowstyle='-',lw=0.35,color=light))

# Save final-size derivatives
fig.savefig(out/'ACS_Nano_TOC_Graphic.png',dpi=600,facecolor='white',bbox_inches=None,pad_inches=0)
fig.savefig(out/'ACS_Nano_TOC_Graphic.tif',dpi=600,facecolor='white',bbox_inches=None,pad_inches=0,pil_kwargs={'compression':'tiff_lzw'})
fig.savefig(out/'ACS_Nano_TOC_Graphic.eps',format='eps',facecolor='white',bbox_inches=None,pad_inches=0)
plt.close(fig)
