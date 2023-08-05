function gfind,lon,lat,pind=pind,rms=rms,noise=noise,$
         par=par,lonr=lonr,latr=latr


; This function helps find a latitude and longitude in
; the gaussian components structure.
;
;  INPUT
;   lon     Longitude to search for
;   lat     Latitude to search for
;   lonr    Two element array of longitude limits, lonr=[lonmin,lonmax]
;   latr    Two element array of latitude limits, latr=[latmin,latmax]
;
;  OUTPUT
;   flag    The function value is either 0 or 1:
;             1 - the position exists in the structure
;             0 - the position does NOT exist in the structure
;            -1 - any problems
;   pind     Index of position in !gstruc.
;   rms     RMS of gaussian fit at the desired position
;   noise   Noise level at desired position
;   par     Parameters of gaussians in gstruc with the desired position
;
; When there are any problems in this program it returns:
;  flag = -1
;  rms = -1
;  noise = -1
;  par = -1
;  pind = -1
;
; Created by David Nidever April 2005

; assume bad until proven otherwise
flag = -1
rms = -1
noise = -1
par = -1
pind = -1

nlon = n_elements(lon)
nlat = n_elements(lat)

; Bad Input Values
if (n_params() eq 0) or (nlon eq 0) or (nlat eq 0) then begin
  print,'Syntax - f = gfind(lon,lat,pind=pind,rms=rms,noise=noise,'
  print,'                   par=par,lonr=lonr,latr=latr)'
  return,-1
endif

; Making sure it's the right structure
;tags = tag_names(!gstruc.data)
;if (n_elements(tags) ne 6) then return,-1
;comp = (tags eq ['LON','LAT','RMS','NOISE','PAR','SIGPAR'])
;if ((where(comp ne 1))(0) ne -1) then return,-1

; setting the ranges
if keyword_set(lonr) then begin
  lon0 = lonr(0)
  lon1 = lonr(1)
endif else begin
  lon0 = 0.
  lon1 = 359.5
endelse
if keyword_set(latr) then begin
  lat0 = latr(0)
  lat1 = latr(1)
endif else begin
  lat0 = -90.
  lat1 = 90.
endelse

if (lon lt lon0) or (lon gt lon1) or (lat lt lat0) or (lat gt lat1) then begin
  flag = -1
  rms = -1
  noise = -1
  par = -1
  pind = -1
  return,flag
endif

;; No !gstruc yet, first position
DEFSYSV,'!gstruc',exists=gstruc_exists
if gstruc_exists eq 0 then begin
  rms = -1
  noise = -1
  par = -1
  pind = -1
  flag = 0
  return,flag
endif

; Looking for the position
t0 = systime(1)
;; LONSTART/LATSTART has a value for each position, faster searching
;;  use NGAUSS and INDSTART to get the indices into DATA
pind = where(*(!gstruc.lonstart) eq lon and *(!gstruc.latstart) eq lat,npind)
print,'find ',systime(1)-t0

; Found something, getting the values
if npind gt 0 then begin
  ind = l64indgen((*(!gstruc.ngauss))[pind[0]])+(*(!gstruc.indstart))[pind[0]]
  rms = first_el((*(!gstruc.data))[ind].rms)
  noise = first_el((*(!gstruc.data))[ind].noise)
  par = ((*(!gstruc.data))[ind].par)(*)
  flag = 1

;; Nothing found
endif else begin
  rms = -1
  noise = -1
  par = -1
  flag = 0
endelse

return,flag

end
