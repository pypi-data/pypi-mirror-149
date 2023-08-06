function getpars,lon,lat,pind=pind

; Return the Gaussian parameters at the given LON/LAT position
; or with the position index PIND.
;
;  INPUT
;   lon     Longitude to search for
;   lat     Latitude to search for
;   =pind   Positions index in !gstruc.
;
;  OUTPUT
;   par     Parameters of gaussians in gstruc with the desired position .
;
; Created by David Nidever Feb 2020

nlon = n_elements(lon)
nlat = n_elements(lat)

; Bad Input Values
if ((nlon eq 0) or (nlat eq 0)) and n_elements(pind) eq 0 then begin
  print,'Syntax - par = getpars(lon,lat,pind=pind)'
  return,-1
endif

;; No !gstruc yet, first position
DEFSYSV,'!gstruc',exists=gstruc_exists
if gstruc_exists eq 0 then return,-1

; Looking for the position
;; LONSTART/LATSTART has a value for each position, faster searching
;;  use NGAUSS and INDSTART to get the indices into DATA
pind = where(*(!gstruc.lonstart) eq lon and *(!gstruc.latstart) eq lat,npind)

; Found something, getting the values
if npind gt 0 then begin
  ind = l64indgen((*(!gstruc.ngauss))[pind[0]])+(*(!gstruc.indstart))[pind[0]]
  par = ((*(!gstruc.data))[ind].par)(*)
  return, par

;; Nothing found
endif else return,-1


end
