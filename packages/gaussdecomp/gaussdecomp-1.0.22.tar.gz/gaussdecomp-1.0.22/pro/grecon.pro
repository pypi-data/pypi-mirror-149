pro grecon,cube,larr,barr,v,file=file,gstruc=gstruc,xr=xr,yr=yr

; This program reconstructs the datacube
; from the results of the gaussian analysis

; getting structure
if not keyword_set(gstruc) then begin
  if not keyword_set(file) then file='hi1d.dat'
  restore,file
endif

lmin = min(gstruc.glon)
lmax = max(gstruc.glon)
bmin = min(gstruc.glat)
bmax = max(gstruc.glat)
nl = (lmax-lmin)*2.+1.
nb = (bmax-bmin)*2.+1.
restore,'lbv_coords.dat'
nv = n_elements(v)

larr = findgen(nl)*0.5+lmin
barr = findgen(nb)*0.5+bmin

cube = fltarr(nl,nv,nb)

; looping through the latitudes
for i=0,nb-1 do begin
  lat = i*0.5+bmin

  ; looping through the longitudes
  for j=0,nl-1 do begin
    lon = j*0.5+lmin

    ind = where(gstruc.glon eq lon and gstruc.glat eq lat,nind)

    if nind gt 0 then begin
      par = (gstruc(ind).par)(*)

      f = gfunc(v,par)
      cube(j,*,i) = f

      ;stop

    end

  end
end

;stop

end
