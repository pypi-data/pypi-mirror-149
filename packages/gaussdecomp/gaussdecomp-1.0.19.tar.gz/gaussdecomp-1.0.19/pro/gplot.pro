pro gplot,v,y,par,color=color,save=save,file=file,$
          yrange=yrange,xrange=xrange,tit=tit,noresid=noresid,$
          xthick=xthick,ythick=ythick,charsize=charsize,charthick=charthick,$
          thick=thick,xtit=xtit,ytit=ytit,position=position,$
          normal=normal,device=device,noerase=noerase,noannot=noannot

; Plots the gaussian fit.  You can plot just the gaussians
; by typing: gplot,v,0,par  (or anything for spec)
;
;  INPUT
;   v        Array of velocities
;   y        Array of spectral points
;   par      Array of gaussian parameters
;   /color   Plot in color
;   /save    Save to postscript file
;   file     Name of postscript file
;   xrange   Range of x-values
;   yrange   Range of y-values
;   tit      Plot title
;   /noresid Don't overplot the residuals
;
;  OUTPUT
;   None
;
; Created by David Nidever April 2005

nv = n_elements(v)
ny = n_elements(y)
npar = n_elements(par)

; In case y is not set you 
;  can still plot the gaussians by themselves
if (ny lt nv) then y = v*0.
ny = n_elements(y)

; Bad Input Values
if (n_params() eq 0) or (nv eq 0) or (ny eq 0) then begin
  print,'Syntax - gplot,v,y,par,color=color,save=save,file=file,'
  print,'         yrange=yrange,xrange=xrange,tit=tit'
  return
endif


if not keyword_set(file) then file='gaussfit'
if keyword_set(save) then ps_open,file,color=color

; colors for my screen
red = 250
lred = 210
green = 190000
orange = 310000
yellow = 450000
blue = -25000
lblue = -15000
purple = -20000
white = -1
backgr = 0.
coarr = [green,lblue,yellow,blue,purple,lred,orange]

; setting for postscript
if keyword_set(color) then begin
  loadct,39
  black=0
  purple=30
  blue=60
  aqua=80
  green=155   ;135
  yellow=200
  orange=225
  white=0
  red=250
  lred=240
  ;backg=white
  backg=yellow
  coarr = [green,aqua,yellow,blue,purple,lred,orange]
endif

ngauss = n_elements(par)/3
if (npar gt 0) then result = gfunc(v,par) else result=y*0.

; Plotting
if not keyword_set(tit) then tit='Gaussian Analysis of HI Spectrum'
if not keyword_set(xtit) then xtit='V!dLSR!n (km s!u-1!n)'
if not keyword_set(ytit) then ytit='T!dB!n (K)'

; Setting the ranges
;dy = max(y)-min(y)
if (stddev(y) ne 0.) then begin
  ;if keyword_set(yrange) then yr=yrange else yr = [min([y,result])-1.0,max([y,result])*1.1]
  if keyword_set(yrange) then yr=yrange else yr = [min([y,result])-3.0,max([y,result])*1.1]
endif else begin
  if keyword_set(yrange) then yr=yrange else yr = [min([y,result])-0.1,max([y,result])*1.1]
endelse
if keyword_set(xrange) then xr=xrange else xr = [min(v),max(v)]
;if keyword_set(yrange) then yr=yrange else yr = [-0.15*dy,max(y)+1]

plot,xr,[0,0],tit=tit,xtit=xtit,ytit=ytit,xr=xr,yr=yr,xstyle=1,ystyle=1,charsize=charsize,$
     xthick=xthick,ythick=ythick,charthick=charthick,thick=thick,position=position,$
     normal=normal,device=device,noerase=noerase
if (ny gt 0) then oplot,v,y,thick=thick
if (npar gt 0) then oplot,v,result+0.02,co=red,thick=thick

; Looping through the gaussians
if ngauss gt 1 then begin
  for i=0,ngauss-1 do begin
    ipar = par(i*3:i*3+2)
    d = where(v ge (ipar(1)-3.5*ipar(2)) and v le (ipar(1)+3.5*ipar(2)),nd)
    g=gfunc(v(d),ipar)
    oplot,v(d),g,co=coarr(i mod 7),linestyle=i/7,thick=thick
  end ;for
endif ;

;overplotting the residuals
if (ny gt 0) and (npar gt 0) and (not keyword_set(noresid)) then begin
  resid = y-result
  if stdev(y) ne 0. then begin 
    ;oplot,v,resid-0.5,thick=thick
    ;oplot,v,v*0.-0.5,thick=thick
    ;xyouts,[xr(0)+0.1*range(xr)],[-0.85],'Residuals',charsize=charsize,charthick=charthick
    oplot,v,resid-2.5,thick=thick
    oplot,v,v*0.-2.5,thick=thick
    ;xyouts,[xr(0)+0.1*range(xr)],[-2.5-0.35],'Residuals',charsize=charsize,charthick=charthick
    xyouts,[xr(0)+0.1*range(xr)],[-1.5],'Residuals',charsize=charsize,charthick=charthick
  end
  ;oplot,v,resid-0.075*dy
endif

; Annotations
if not keyword_set(noannot) then begin
  xyouts,[xr(0)+0.1*range(xr)],[yr(0)+0.9*range(yr)],'Observed HI',charsize=charsize,charthick=charthick
  xyouts,[xr(0)+0.1*range(xr)],[yr(0)+0.86*range(yr)],'Sum of Gaussians',charsize=charsize,charthick=charthick,co=red
endif

if keyword_set(save) then ps_close

;stop

end
