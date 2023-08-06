pro gstruc_remove,pindex

;; This "removes" indices from gstruc by shifting everything over
;;  this assumes that the IND indices is contiguous (i.e. no gaps)

;; GSTRUC structure:
;;   gaussian data
;; DATA      pointer to NDATA-sized Gaussian structure  contains the actual Gaussian information
;; NDATA     integer  number of total elements in DATA
;; COUNT     integer  number of elements filled in DATA
;; REVINDEX  pointer to NDATA-sized array  reverse index, takes you from data index to lonstart/latstart/ngauss
;;   positional data  
;; LONSTART  pointer to NDATA-sized array  longitude of this position, one element per position
;; LATSTART  pointer to NDATA-sized array  latitude of this position, one element per position
;; NGAUSS    pointer to NDATA-sized array  number of Gaussians at this position, one element per position
;; INDSTART  pointer to NDATA-sized array  the index in DATA where the Gaussians for this position start
;; PCOUNT    integer   the number of unique spatial positions

;; data: large data structure
;; ndata: number of elements of data
;  count:  the number of elements in DATA were using currently, also
;           the index of the next one to stat with.
;; revindex: reverse index, takes you from data index to lonstart/latstart/ngauss
;; lonstart/latstart/ngauss: give the lon/lat value at the start of a
;;            sequence of Gaussians, and the number of gaussians
;; indstart: the index in DATA where the gaussians for this position start
;; pcount: the number of spatial positions

pind = first_el(pindex)  ;; in case it's a one-element array

;; Get the indices into DATA
ind = l64indgen( (*!gstruc.ngauss)[pind] ) + (*!gstruc.indstart)[pind]


nind = n_elements(ind)
rem0 = min(ind)
rem1 = max(ind)

ndtags = n_tags(*(!gstruc.data))

;; UPDATE DATA
;; At the end, nothing to shift, just zero-out
if rem1 eq !gstruc.count-1 then begin
  ;; Zero out the removed elements
  temp = *(!gstruc.data)
  for i=0,ndtags-1 do temp[rem0:rem1].(i) = 999999.
  !gstruc.data = ptr_new(temp)
  undefine,temp

;; Shift everything above REM1 to start at REM0
endif else begin
  above0 = rem1+1
  above1 = !gstruc.count-1
  nabove = above1-above0+1
  data = *(!gstruc.data)
  temp = data[above0:above1]
  ;; Zero out the old positions
  for i=0,ndtags-1 do data[above0:above1].(i)=999999.
  ;; Zero out the data we are removing
  for i=0,ndtags-1 do data[ind].(i)=999999.
  ;; Stuff the data in the new positions
  data[rem0:rem0+nabove-1] = temp
  !gstruc.data = ptr_new(data)
  undefine,data
endelse

;; UPDATE LONSTART/LATSTART/NGAUSS arrays
;; lonstart, latstart, indstart, ngauss, pcount
;; Use REVINDEX
;; At the end, nothing to shift, just zero-out
if pind eq !gstruc.pcount-1 then begin
  ;; Zero out the remaining elements
  ;; lonstart
  lonstart = *(!gstruc.lonstart)
  lonstart[pind] = 999999.
  !gstruc.lonstart = ptr_new(lonstart)
  undefine,lonstart
  ;; latstart
  latstart = *(!gstruc.latstart)
  latstart[pind] = 999999.
  !gstruc.latstart = ptr_new(latstart)
  undefine,latstart
  ;; indstart
  indstart = *(!gstruc.indstart)
  indstart[pind] = -1
  !gstruc.indstart = ptr_new(indstart)
  undefine,indstart
  ;; ngaus
  ngaus = *(!gstruc.ngauss)
  ngauss[pind] = -1
  !gstruc.ngauss = ptr_new(ngauss)
  undefine,ngauss

;; Shift everything above PREM1 to start at PREM0
endif else begin
  pabove0 = pind+1
  pabove1 = !gstruc.pcount-1
  npabove = pabove1-pabove0+1
  ;; LONSTART
  lonstart = *(!gstruc.lonstart)
  temp_lonstart = lonstart[pabove0:pabove1]
  lonstart[pabove0:pabove1] = 999999.
  lonstart[pind:pind+npabove-1] = temp_lonstart
  !gstruc.lonstart = ptr_new(lonstart)
  undefine,lonstart,temp_lonstart
  ;; LATSTART
  latstart = *(!gstruc.latstart)
  temp_latstart = latstart[pabove0:pabove1]
  latstart[pabove0:pabove1] = 999999.
  latstart[pind:pind+npabove-1] = temp_latstart
  !gstruc.latstart = ptr_new(latstart)
  undefine,latstart,temp_latstart
  ;; INDSTART
  indstart = *(!gstruc.indstart)
  temp_indstart = indstart[pabove0:pabove1]
  indstart[pabove0:pabove1] = -1
  indstart[pind:pind+npabove-1] = temp_indstart
  !gstruc.indstart = ptr_new(indstart)
  undefine,indstart,temp_indstart
  ;; NGAUSS
  ngauss = *(!gstruc.ngauss)
  temp_ngauss = ngauss[pabove0:pabove1]
  ngauss[pabove0:pabove1] = -1
  ngauss[pind:pind+npabove-1] = temp_ngauss
  ;; Renumber NGAUSS
  ;;  convert the old index to the new index
  ;;  newindex = converter[oldindex]
  indtokeep = l64indgen(!gstruc.pcount)
  REMOVE,pind,indtokeep
  index_converter = lon64arr(!gstruc.pcount)-1
  index_converter[indtokeep] = l64indgen(!gstruc.pcount-1)
  ;; only convert the ones that were moved
  moved_old_ngauss_values = ngauss[pind:pind+npabove-1]
  ngauss[pind:pind+npabove-1] = index_converter[moved_old_ngauss_values]
  !gstruc.ngauss = ptr_new(ngauss)
  undefine,ngauss,temp_ngauss
endelse

;; UPDATE REVINDEX
;;  shift them first

;; At the end, nothing to shift, just zero-out
if rem1 eq !gstruc.count-1 then begin
  revindex = *(!gstruc.revindex)
  revindex[ind] = -1  ; zero out the removed elements
  !gstruc.revindex = ptr_new(revindex)
  undefine,revindex

;; Shift everything above REM1 to start at REM0
endif else begin
  above0 = rem1+1
  above1 = !gstruc.count-1
  nabove = above1-above0+1
  revindex = *(!gstruc.revindex)
  temp = revindex[above0:above1]
  ;; Zero out the old positions
  revindex[above0:above1] = -1
  ;; Zero out the data we are removing
  revindex[ind] = -1
  ;; Stuff the data in the new positions
  revindex[rem0:rem0+nabove-1] = temp
  ;; Renumber REVINDEX
  ;;  convert the old index to the new index
  ;;  newindex = convert[oldindex]
  indtokeep = l64indgen(!gstruc.count)
  REMOVE,ind,indtokeep
  index_converter = lon64arr(!gstruc.count)-1
  index_converter[indtokeep] = l64indgen(!gstruc.count-nind)
  ;; only convert the ones that were moved
  moved_old_revindex_values = revindex[rem0:rem0+nabove-1]
  revindex[rem0:rem0+nabove-1] = index_converter[moved_old_revindex_values]
  !gstruc.revindex = ptr_new(revindex)
  undefine,revindex
endelse

;; Reduce counters
!gstruc.pcount--
!gstruc.count -= nind

end
