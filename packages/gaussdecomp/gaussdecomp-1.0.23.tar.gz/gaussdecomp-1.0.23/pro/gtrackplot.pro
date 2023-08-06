pro gtrackplot,lon,lat,lastlon,lastlat,redo,count,lonr=lonr,latr=latr,$
               save=save,pstr=pstr,xstr=xstr,ystr=ystr

; This program plots the progression of the
; gaussian analysis in gdriver.pro
;
;  INPUT
;   lon     Current longitude
;   lat     Current latitude
;   redo    Redo parameter
;   count   Count
;   lonr    Two element array of longitude limits
;   latr    Two element array of latitude limits
;   /save   Save plot to postscript file
;   pstr    The !P plotting structure
;   xstr    The !X plotting structure
;   ystr    The !Y plotting structure
;
;  OUTPUT
;   None
;
; COLORS
;  white    to be done
;  green    have been done/visited
;  yellow     current, normal
;  red      current, redo
;
; Created by David Nidever April 2005

nlon = n_elements(lon)
nlat = n_elements(lat)
nredo = n_elements(redo)
ncount = n_elements(count)

; Bad Input Values
if (n_params() eq 0) or (nlon eq 0) or (nlat eq 0) or (nredo eq 0) or $
     (ncount eq 0) then begin
  print,'Syntax - gtrackplot,lon,lat,redo,count,lonr=lonr,'
  print,'                    latr=latr,save=save'
  return
endif

; Making sure it's the right structure
tags = tag_names(*(!gstruc.data))
if (n_elements(tags) ne 6) then return
comp = (tags eq ['LON','LAT','RMS','NOISE','PAR','SIGPAR'])
if ((where(comp ne 1))(0) ne -1) then return

color=1

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
coarr = [green,orange,yellow,blue,purple,lred,lblue]

; setting for postscript
if keyword_set(save) then begin
  loadct,13
  black=0
  purple=30
  blue=60
  aqua=80
  green=135   ;155   ;135
  yellow=200
  orange=225
  white=0
  red=240  ; 300
  lred=240
  ;backg=white
   backg=yellow
  coarr = [green,orange,yellow,blue,purple,lred,aqua]
endif

if keyword_set(save) then ps_open,'gtrackplot',color=color

if (n_elements(lonr) eq 0) then lonr = [0.,395.5]
if (n_elements(latr) eq 0) then latr = [-90.,90.]
if (n_elements(count) eq 0) then count = -1

nlon = (lonr(1)-lonr(0))*2 + 1
nlat = (latr(1)-latr(0))*2 + 1
larr = findgen(nlon)*0.5+lonr(0)
barr = findgen(nlat)*0.5+latr(0)

;psym8,1.5
psym8,0.8
loadct,13

;plot the grid
if (count eq 1) then begin
  window,1,xsize=nlon*5<1000,ysize=nlat*5<1000,xpos=0,ypos=600

  plot,dist(5),/nodata,xr=[lonr(0)-0.5,lonr(1)+0.5],yr=[latr(0)-0.5,latr(1)+0.5],xstyle=1,ystyle=1,$
       xtit='Longitude',ytit='Latitude',tit='Tracking the Gaussian Analysis        '

  ;for i=0,nlon-1 do oplot,[larr(i),larr(i)],latr
  ;for i=0,nlat-1 do oplot,lonr,[barr(i),barr(i)]

  ; points still to be done (all points really)
  for i=0,nlat-1 do oplot,larr,fltarr(nlon)+barr(i),ps=3,co=white
  ;for i=0,nlat-1 do oplot,larr,fltarr(nlon)+barr(i),ps=8,co=white

  ;stop

  ; overplotting the points already completed
  DEFSYSV,'!gstruc',exists=gstruc_exists
  if gstruc_exists then begin
    larr2 = (*(!gstruc.data)).lon
    barr2 = (*(!gstruc.data)).lat
    oplot,larr2,barr2,ps=8,co=green
    ;oplot,larr2,barr2,ps=8,co=green

    ;stop
 
    ;lmin = min(gstruc.lon)
    ;lmax = max(gstruc.lon)
    ;bmin = min(gstruc.lat)
    ;bmax = max(gstruc.lat)
    ;nl = (lmax-lmin)*2+1
    ;nb = (bmax-bmin)*2+1
    ;
    ;for i=0,nl-1 do begin
    ;  ll = lmin+i*0.5
    ;  for j=0,nb-1 do begin
    ;    bb = bmin+j*0.5
    ;    dum = where(gstruc.lon eq ll and gstruc.lat eq bb,ndum)
    ;    if ndum gt 0 then oplot,[ll],[bb],ps=8,co=190000   ; green
    ;  end
    ;end
  endif

end ; count=0


; Re-setting the window and plotting state
wset,1
if keyword_set(pstr) then !p = pstr
if keyword_set(xstr) then !x = xstr
if keyword_set(ystr) then !y = ystr

; overplotting our point
; white for normal, red for redo
;if redo eq 0 then co=yellow else co=red
co = red
oplot,[lastlon],[lastlat],ps=8,co=green
oplot,[lon],[lat],ps=8,co=co

xyouts,0.8,0.98,'count='+strtrim(count-1,2),co=backgr,/normal,charsize=1.2
xyouts,0.8,0.98,'count='+strtrim(count,2),/normal,charsize=1.2

if keyword_set(save) then ps_close

; Saving the plotting state
pstr = !p
xstr = !x
ystr = !y

; Setting it back to window 0 for the regular plot
wset,0

;stop

end
