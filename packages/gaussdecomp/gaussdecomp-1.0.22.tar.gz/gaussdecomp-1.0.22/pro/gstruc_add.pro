pro gstruc_add,tstr
;;  This adds new elements to gstruct

ntstr = n_elements(tstr)

gstruc_schema = {lon:999999.,lat:999999.,rms:999999.,noise:999999.,$
                 par:fltarr(3)+999999.,sigpar:fltarr(3)+999999.,glon:999999.,glat:999999.}

DEFSYSV,'!gstruc',exists=gstruc_exists
if not keyword_set(gstruc_exists) then begin
  DEFSYSV,'!gstruc',{data:ptr_new(),ndata:0LL,count:0LL,revindex:ptr_new(),lonstart:ptr_new(),$
                     latstart:ptr_new(),indstart:ptr_new(),ngauss:ptr_new(),pcount:0LL}
  !gstruc.data = ptr_new(replicate(gstruc_schema,100000L))
  !gstruc.ndata = 100000LL
  !gstruc.count = 0LL
  !gstruc.revindex = ptr_new(lon64arr(100000L)-1)
  !gstruc.lonstart = ptr_new(fltarr(100000L)+999999)
  !gstruc.latstart = ptr_new(fltarr(100000L)+999999)
  !gstruc.indstart = ptr_new(lon64arr(100000L)-1)
  !gstruc.ngauss = ptr_new(lonarr(100000L)-1)
  !gstruc.pcount = 0LL
endif
;; data: large data structure
;; ndata: number of elements of data
;  count:  the number of elements in DATA were using currently, also
;           the index of the next one to stat with.
;; revindex: reverse index, takes you from data index to lonstart/latstart/ngauss
;; lonstart/latstart/ngauss: give the lon/lat value at the start of a
;;            sequence of Gaussians, and the number of gaussians
;; indstart: the index in DATA where the gaussians for this position start
;; pcount: the number of spatial positions

;; Add new elements
if ntstr+!gstruc.count gt !gstruc.ndata then begin
  print,'Adding more elements to GSTRUC'
  ;; Old structures/arrays
  data = *(!gstruc.data)
  ndata = !gstruc.ndata
  count = !gstruc.count
  revindex = *(!gstruc.revindex)
  lonstart = *(!gstruc.lonstart)
  latstart = *(!gstruc.latstart)
  indstart = *(!gstruc.indstart)
  ngauss = *(!gstruc.ngauss)
  pcount = !gstruc.pcount
  ;; Make new structures/arrays
  new_data = replicate(gstruc_schema,ndata+100000L)
  new_ndata = long64(n_elements(new_data))
  new_revindex = lon64arr(ndata+100000L)-1
  new_lonstart = fltarr(ndata+100000L)+999999.
  new_latstart = fltarr(ndata+100000L)+999999.
  new_indstart = lon64arr(ndata+100000L)-1
  new_ngauss = lonarr(ndata+100000L)-1
  ;; Stuff in the old values
  new_data[0:ndata-1] = data
  new_revindex[0:ndata-1] = revindex
  new_lonstart[0:ndata-1] = lonstart
  new_latstart[0:ndata-1] = latstart
  new_indstart[0:ndata-1] = indstart
  new_ngauss[0:ndata-1] = ngauss
  ;; Put it into !gstruc
  !gstruc.data = ptr_new(new_data)
  !gstruc.ndata = new_ndata
  !gstruc.count = count
  !gstruc.revindex = ptr_new(new_revindex)
  !gstruc.lonstart = ptr_new(new_lonstart)
  !gstruc.latstart = ptr_new(new_latstart)
  !gstruc.indstart = ptr_new(new_indstart)
  !gstruc.pcount = pcount
endif

;; Stuff in the new data
;; data
temp = *(!gstruc.data)
temp[!gstruc.count:!gstruc.count+ntstr-1] = tstr
!gstruc.data = ptr_new(temp)
undefine,temp
;; revindex
temp = *(!gstruc.revindex)
temp[!gstruc.count:!gstruc.count+ntstr-1] = !gstruc.pcount
!gstruc.revindex = ptr_new(temp)
undefine,temp
;; lonstart
temp = *(!gstruc.lonstart)
temp[!gstruc.pcount] = tstr[0].lon
!gstruc.lonstart = ptr_new(temp)
undefine,temp
;; latstart
temp = *(!gstruc.latstart)
temp[!gstruc.pcount] = tstr[0].lat
!gstruc.latstart = ptr_new(temp)
undefine,temp
;; indstart
temp = *(!gstruc.indstart)
temp[!gstruc.pcount] = !gstruc.count
!gstruc.indstart = ptr_new(temp)
undefine,temp
;; ngauss
temp = *(!gstruc.ngauss)
temp[!gstruc.pcount] = ntstr
!gstruc.ngauss = ptr_new(temp)
undefine,temp
;; counters
!gstruc.count += ntstr
!gstruc.pcount += 1

end
