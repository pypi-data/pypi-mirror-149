pro gpeak1,smresid,top,maxarr

; Gets peaks

  ; getting maxima
  maxmin,smresid,minarr,maxarr
  if maxarr(0) ne -1 then begin
    gd = where(smresid[maxarr] gt top,ngd)
    if ngd gt 0 then begin
      maxarr = maxarr[gd]
    endif else begin
      maxarr = -1
    endelse
  endif

;stop

end
