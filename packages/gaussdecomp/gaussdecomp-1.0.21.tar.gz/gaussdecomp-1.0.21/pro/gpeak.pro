pro gpeak,smresid4,smresid16,top,maxarr

; Gets peaks
;
;  INPUT
;   smresid4   Array of smoothed residuals (4)
;   smresid16  Array of smoothed residuals (16)
;   top        Height threshold
;
;  OUTPUT
;   maxarr   Array of maxima
;
; When there is a problem in this program it returns:
;  maxarr = -1
;
; Created by David Nidever April 2005

nsm4 = n_elements(smresid4)
nsm16 = n_elements(smresid16)
ntop = n_elements(top)

; Bad Input Values
if (n_params() eq 0) or (nsm4 eq 0) or (nsm16 eq 0) or $
     (ntop eq 0) then begin
  print,'Syntax - gpeak,smresid4,smresid16,top,maxarr'
  return
endif

; Getting maxima
maxmin,smresid4,minarr4,maxarr4
maxmin,smresid16,minarr16,maxarr16
;maxspec = max(y)
;nn = 3.

; Points above threshold
if (maxarr4(0) ne -1) then gd4 = where(smresid4(maxarr4) gt top,ngd4) $
  else ngd4 = 0
if (maxarr16(0) ne -1) then gd16 = where(smresid16(maxarr16) gt top,ngd16) $
  else ngd16 = 0
; if ngd4 eq 0 and ngd16 eq 0 then begin
;   nn = 2.
;   gd4 = where(resid(maxarr4) gt nn*noise,ngd4)
;   gd16 = where(resid(maxarr16) gt nn*noise,ngd16)
; endif

;gd = where(y(maxarr) gt 0.05*maxspec,ngd)

; Remove maxima from wide spec that are in narrow spec
if ngd16 gt 0 and ngd4 gt 0 then begin
  for j=0,ngd16-1 do begin
     clos = min(abs(maxarr4(gd4)-maxarr16(gd16(j))))
     if clos lt 4 then gd16(j) = -1
  endfor

  ; Removing duplicates
  badind = where(gd16 eq -1, nbadind)
  if nbadind eq ngd16 then begin
    gd16 = [-1]
    ngd16 = 0
  endif else begin
    ;if nbadind gt 1 then remove,badind,gd16
    if nbadind gt 0 then remove,badind,gd16
    ngd16 = n_elements(ngd16)
  endelse
endif

If (ngd4 gt 0) or (ngd16 gt 0) then begin

  ; Putting the two maxarr's together
  if ngd16 gt 0 then begin
    maxarr = [maxarr4(gd4),maxarr16(gd16)]
    y = [smresid4(maxarr4(gd4)),smresid16(maxarr16(gd16))]  ; height for sorting
  endif else begin
    maxarr = maxarr4(gd4)
    y = smresid4(maxarr4(gd4))
  endelse

  ; Sorting, getting tallest ones first
  si = sort(y)
  maxarr = maxarr(si)

  ;si4 = sort(resid(maxarr4(gd4)))
  ;gd4 = gd4(reverse(si4))
  ;if ngd16 gt 0 then begin
  ;  si16 = sort(resid(maxarr16(gd16)))
  ;  gd16 = gd16(reverse(si16))
  ;endif
  ; ngd = ngd4 + ngd16

Endif else begin
  maxarr=-1
Endelse

;stop

end
