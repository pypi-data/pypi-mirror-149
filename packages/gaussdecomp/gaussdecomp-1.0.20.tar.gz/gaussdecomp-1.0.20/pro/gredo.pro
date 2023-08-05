function gredo,lon,lat,guesslon,guesslat,guesspar

; This function checks wether we can redo this location again
; returns 1 if this redo is okay
; returns 0 if this redo is NOT okay
;
;  INPUT
;   lon       Longitude of current position
;   lat       Latitude of current position
;   guesslon  Longitude of guess position
;   guesslat  Latitude of guess position
;   guesspar  Guess parameters
;
;  OUTPUT
;   flag      Function value is either:
;              1 - Redo okay. This guess has not been done before
;              0 - Redo NOT okay. This guess has been done before
;
; When there are any problems in this program it returns:
;  flag = -1
;
; Created by David Nidever April 2005

; bad to start out with
flag = -1

nlon = n_elements(lon)
nlat = n_elements(lat)
nglon = n_elements(guesslon)
nglat = n_elements(guesslat)
ngpar = n_elements(guesspar)

; Bad Input Values
if (n_params() eq 0) or (nlon eq 0) or (nlat eq 0) and (nglon eq 0) or $
     (nglat eq 0) or (ngpar eq 0) then begin
  print,'Syntax - redo = gredo(lon,lat,guesslon,guesslat,guesspar)'
  return,-1
endif

; Making sure it's the right structure
tags = tag_names(*(!btrack.data))
if (n_elements(tags) ne 15) then return,-1
btags = ['COUNT','LON','LAT','RMS','NOISE','PAR','GUESSPAR','GUESSLON','GUESSLAT'$
       ,'BACK','REDO','REDO_FAIL','SKIP','LASTLON','LASTLAT']
comp = (tags eq btags)
if ((where(comp ne 1))(0) ne -1) then return,-1


flag = 1   ; do it unless proven wrong

; FROM **ANY** PREVIOUS POSITION
prev = where((*(!btrack.data)).lon eq lon and (*(!btrack.data)).lat eq lat, nprev)

;prev = where(btrack.lon eq lon and btrack.lat eq lat $
;             and btrack.guesslon eq guesslon and btrack.guesslat eq guesslat, nprev)

gd1 = where(guesspar ne 999999.,ngd1)
if (ngd1 eq 0) then begin
  flag = 0
  goto, BOMB
endif
tguesspar = guesspar(gd1)
nguesspar = n_elements(tguesspar)
ngg = nguesspar/3

; FROM **ANY** PREVIOUS POSITION
; we have used a guess from this position before
;  but have the parameters changed sufficiently
if (nprev gt 0) then begin

  ; Looping through the previous ones
  for i=0,nprev-1 do begin
    guesspar2 = (*(!btrack.data))[prev[i]].guesspar
    gd2 = where(guesspar2 ne 999999.,ngd2)
   
    ; some gaussians found
    if (ngd2 gt 0) then begin
      tpar = guesspar2(gd2)
      ntpar = n_elements(tpar)
      ntg = ntpar/3          ; # of gaussians in this guess

      ; same number of gaussians
      if (ntpar eq nguesspar) then begin

        ; sorting, largest first
        tpar2 = gsort(tpar)
        tguesspar2 = gsort(tguesspar)

        ; fixing possible zeros that could ruin the ratio
        dum = tpar2
        bd = where(dum eq 0.,nbd)
        if nbd gt 0 then dum(bd) = 1d-5

        diff = abs(tpar2 - tguesspar2)
        ratio = diff/abs(dum)

        ; These differences are too small, NO redo
        if (max(ratio) lt 0.01) then begin
          flag = 0
          goto,BOMB
        endif
      endif  ; ntg eq ngg
    endif  ; some gaussians found
  endfor  ; looping through the guesses

endif  ; we've tried this before

BOMB:

;stop

return,flag

end
