pro gguess,lon,lat,guesspar,guesslon,guesslat,lonsgn=lonsgn,latsgn=latsgn,$
           lonr=lonr,latr=latr

; This program finds the best guess for the new profile
; The one from the backwards positions.
; If it can't find one then it returns 999999.'s
;
;  INPUT
;   lon      Longitude of current position
;   lat      Latitude of current position
;   lonsgn   Sign of longitude increment
;   latsgn   Sign of latitude increment
;   lonr     Two element array of longitude limits
;   latr     Two element array of latitude limits
;
;  OUTPUT
;   guesspar  The first guess gaussian parameters
;   guesslon  The longitude of the position where the
;               guess parameters came from
;   guesslat  The latitude of the position where the
;               guess parameters came from
;
; When this program has problems it returns:
;  guesspar = 999999.
;  guesslon = 999999.
;  guesslat = 999999.
;
; Created by David Nidever April 2005

; bad until proven okay
guesspar = 999999.
guesslon = 999999.
guesslat = 999999.

nlon = n_elements(lon)
nlat = n_elements(lat)

; Bad Input Values
if (n_params() eq 0) or (nlon eq 0) or (nlat eq 0) then begin
  print,'Syntax - gguess,lon,lat,guesspar,guesslon,guesslat,'
  print,'                lonsgn=lonsgn,latsgn=latsgn,lonr=lonr,latr=latr'
  return
endif

; Making sure it's the right structure
tags = tag_names(*(!gstruc.data))
if (n_elements(tags) ne 6) then return
comp = (tags eq ['LON','LAT','RMS','NOISE','PAR','SIGPAR'])
if ((where(comp ne 1))(0) ne -1) then return

; saving the originals
orig_lon = lon
orig_lat = lat

if not keyword_set(lonsgn) then lonsgn=1.
if not keyword_set(latsgn) then latsgn=1.

if not keyword_set(lonr) then lonr = [0.,359.5]
if not keyword_set(latr) then latr = [-90.,90.]

; Is the longitude range continuous??
if (lonr(0) eq 0.) and (lonr(1) eq 359.5) then cont=1 else cont=0

; getting the p3 and p4 positions
; P3 back in longitude (l-0.5), same latitude
; P4 back in latitude (b-0.5), same longitude
gincrement,lon,lat,lon3,lat3,lonsgn=-lonsgn,latsgn=-latsgn,lonr=lonr,latr=latr  
gincrement,lon,lat,lon4,lat4,lonsgn=lonsgn,latsgn=-latsgn,lonr=lonr,latr=latr,/p2

;p3 = gfind(gstruc,lon-lonsgn*0.5,lat,ind=ind3,rms=rms3,noise=noise3,par=par3)
;p4 = gfind(gstruc,lon,lat-latsgn*0.5,ind=ind4,rms=rms4,noise=noise4,par=par4)

; CHECKING OUT THE EDGES
; AT THE LEFT EDGE, and continuous, Moving RIGHT, use neighbor on other side
; Use it for the guess, but never move to it directly
if (lon eq lonr(0)) and (lonsgn eq 1) and (cont eq 1) then begin
  lat3 = lat
  lon3 = lonr(1)
endif

; AT THE RIGHT EDGE, and continuous, Moving LEFT
if (lon eq lonr(1)) and (lonsgn eq -1) and (cont eq 1) then begin
  lat3 = lat
  lon3 = lonr(0)
endif

; At the edge, NOT continuous, Moving RIGHT, NO P3 NEIGHBOR
if (lon eq lonr(0)) and (lonsgn eq 1) and (cont eq 0) then begin
  lon3 = 999999.
  lat3 = 999999.
end

; At the edge, NOT continuous, Moving LEFT, NO P3 NEIGHBOR
if (lon eq lonr(1)) and (lonsgn eq -1) and (cont eq 0) then begin
  lon3 = 999999.
  lat3 = 999999.
end

; Have they been visited before?
p3 = gfind(lon3,lat3,ind=ind3,rms=rms3,noise=noise3,par=par3)
p4 = gfind(lon4,lat4,ind=ind4,rms=rms4,noise=noise4,par=par4)

; Comparing the solutions
b34 = gbetter(par3,rms3,noise3,par4,rms4,noise4)

; selecting the best guess
if (b34 eq 0) then begin  ; using P3
  guesspar = par3
  ;guesslon = lon-lonsgn*0.5
  ;guesslat = lat
  guesslon = lon3
  guesslat = lat3
endif
if (b34 eq 1) then begin  ; using P4
  guesspar = par4
  ;guesslon = lon
  ;guesslat = lat-latsgn*0.5
  guesslon = lon4
  guesslat = lat4
endif
if (b34 eq -1) then begin
  guesspar = 999999.
  guesslon = 999999.
  guesslat = 999999.
endif

; putting the originals back
lon = orig_lon
lat = orig_lat

;stop

end
