pro gbtrack,btrack,str

; This program increases the size of the parameter array in btrack
; if necessary
;
;  INPUT
;   btrack   The tracking structure
;   str      A "gstruc" structure
;
;  OUTPUT
;   btrack   The tracking structure with larger par/guesspar arrays
;
; Created by David Nidever May 2005

nb = n_elements(btrack)
ns = n_elements(str)

; Bad Input Values
if (n_params() eq 0) or (nb eq 0) or (ns eq 0) then begin
  print,'Syntax - gbtrack,btrac,str'
  return
endif

npar = n_elements((str.par)(*))
nbpar = n_elements(btrack(0).par)

; increasing the space
if (npar gt nbpar) then begin

  ; Starting the tracking structure, bad until proven good
  track = {count:999999.,lon:999999.,lat:999999.,rms:999999.,noise:999999.,par:fltarr(npar)+999999,$
           guesspar:fltarr(npar)+999999.,guesslon:999999.,guesslat:999999.,back:999999.,redo:999999.,$
           redo_fail:999999.,skip:999999.,lastlon:999999.,lastlat:999999.}
  nbtrack = n_elements(btrack)
  newbtrack = replicate(track,nbtrack)

  ; Coping over the info
  newbtrack.count = btrack.count
  newbtrack.lon = btrack.lon
  newbtrack.lat = btrack.lat
  newbtrack.rms = btrack.rms
  newbtrack.noise = btrack.noise
  newbtrack.par(0:nbpar-1) = btrack.par(0:nbpar-1)
  newbtrack.guesspar(0:nbpar-1) = btrack.guesspar(0:nbpar-1)
  newbtrack.guesslon = btrack.guesslon
  newbtrack.guesslat = btrack.guesslat
  newbtrack.back = btrack.back
  newbtrack.redo = btrack.redo
  newbtrack.redo_fail = btrack.redo_fail
  newbtrack.skip = btrack.skip
  newbtrack.lastlon = btrack.lastlon
  newbtrack.lastlat = btrack.lastlat

  ;stop

  btrack = newbtrack

end

;stop

end
