pro gincrement,lon,lat,newlon,newlat,lonr=lonr,latr=latr,$
               lonsgn=lonsgn,latsgn=latsgn,nstep=nstep,p2=p2

; This program increments the position
;
;  INPUT
;   lon      Longitude of current position
;   lat      Latitude of current position
;   lonsgn   Sign of longitude increment
;   latsgn   Sign of latitude increment
;   lonr     Two element array of longitude limits
;   latr     Two element array of latitude limits
;   nstep    Number of steps to increment
;   /p2      Increment in latitude rather than in longtide
;
;  OUTPUT
;   newlon   Longitude of new position
;   newlat   Latitude of new position
;
; When this program has problems it returns:
;  newlon = 999999.
;  newlat = 999999.
;
; Created by David Nidever April 2005

step = 1.0   ; 0.5

; bad until proven okay
newlon = 999999.
newlat = 999999.

nlon = n_elements(lon)
nlat = n_elements(lat)

if (n_params() eq 0) or (nlon eq 0) or (nlat eq 0) then begin
  print,'Syntax - gincrement,lon,lat,newlon,newlat,lonr=lonr,latr=latr,'
  print,'                    lonsgn=lonsgn,latsgn=latsgn,nstep=nstep,p2=p2'
  return
endif


;if not keyword_set(lonr) then lonr = [0.,359.5]
;if not keyword_set(latr) then latr = [-90.,90.]
if n_elements(lonr) eq 0 then lonr = [0.,2000.]
if n_elements(latr) eq 0 then latr = [0.,2000.]

;if not keyword_set(lon0) then lon0 = 0.
;if not keyword_set(lon1) then lon1 = 359.5  ; last lon. to do
;if not keyword_set(lat0) then lat0 = -90.
;if not keyword_set(lat1) then lat1 = 90.   ; last lat. to do
if not keyword_set(lonsgn) then lonsgn=1.
if not keyword_set(latsgn) then latsgn=1.
if not keyword_set(nstep) then nstep=1

; longitude and latitude limits
lon0 = float(lonr(0))
lon1 = float(lonr(1))
lat0 = float(latr(0))
lat1 = float(latr(1))

; are we in the box?
if (lon lt lon0) or (lon gt lon1) or (lat lt lat0) or (lat gt lat1) then begin
  newlon = 999999.
  newlat = 999999.
  goto,BOMB
endif

; wrong signs
if abs(lonsgn) ne 1 then goto,BOMB
if abs(latsgn) ne 1 then goto,BOMB

; figuring out the case
;bit = ((latsgn+1.)*0.5) + 2.*((lonsgn+1.)*0.5)
;bit = long(bit)
;
; bit (lon,lat)
; 0 - (-1,-1)
; 1 - (-1,+1)
; 2 - (+1,-1)
; 3 - (+1,+1)

tlon = float(lon)
tlat = float(lat)

; Looping through all the steps
FOR i=0,nstep-1 do begin

  ; p2, incrementing vertically
  IF keyword_set(p2) then begin

    ; UP, at the end
    if (latsgn eq 1) and (tlat eq lat1) then begin
      newlon = 999999.
      newlat = 999999.
      goto,BOMB
    end
  
    ; DOWN, at the end
    if (latsgn eq -1) and (tlat eq lat0) then begin
      newlon = 999999.
      newlat = 999999.
      goto,BOMB
    end

    ; Not at end, normal increment
    newlon = tlon
    newlat = tlat + latsgn * step

  ; Incrementing Sideways
  ENDIF ELSE BEGIN


    ; RIGHT, lonsgn = +1
    If (lonsgn eq 1) then begin

      ; UP, the very end
      if (latsgn eq 1) and (tlon eq lon1) and (tlat eq lat1) then begin
        newlon = 999999.
        newlat = 999999.
        goto,BOMB
      endif

      ; DOWN, the very end
      if (latsgn eq -1) and (tlon eq lon1) and (tlat eq lat0) then begin
        newlon = 999999.
        newlat = 999999.
        goto,BOMB
      endif

      ; at end of longitude, increment latitude
      if (tlon eq lon1) then begin
        newlon = lon0
        newlat = tlat + latsgn * step
      endif

      ; normal increment
      if (tlon ne lon1) then begin
        newlon = tlon + lonsgn * step
        newlat = tlat
      endif

    Endif ; RIGHT, lonsgn=+1

    ; LEFT, lonsgn = -1
    If (lonsgn eq -1) then begin

      ; UP, the very end
      if (latsgn eq 1) and (tlon eq lon0) and (tlat eq lat1) then begin
          newlon = 999999.
          newlat = 999999.
          goto,BOMB
      endif

      ; DOWN, the very end 
      if (latsgn eq -1) and (tlon eq lon0) and (tlat eq lat0) then begin
        newlon = 999999.
        newlat = 999999.
        goto,BOMB
      endif

      ; at end of longitude, increment latitude
      if (tlon eq lon0) then begin
        newlon = lon1
        newlat = tlat + latsgn * step
      endif

      ; normal increment
      if (tlon ne lon0) then begin
        newlon = tlon + lonsgn * step
        newlat = tlat
      endif

    Endif ; LEFT, lonsgn=-1


  ENDELSE  ; not p2

  ; in case we're looping
  tlon = newlon
  tlat = newlat


END ; looping through steps

; final answer
newlon = tlon
newlat = tlat

BOMB:

;print,newlon,newlat

;stop

end
