program project

  use mpi
  !$use omp_lib
  implicit none
  integer :: L=50, N, N_i, N_j
  integer :: i,j,n_iter,d,  ios, rowtype, rowtype2, lower_bound_j, upper_bound_j, lower_bound_i, upper_bound_i, z
  integer :: ierror, status(MPI_STATUS_SIZE), me, npe, lrank, tag=0, tag2=1, request1(4), request2(4)
  integer, parameter :: comm = MPI_COMM_WORLD, dim=2
  logical :: period_BC(dim), reorder = .true., file_exists
  integer, allocatable :: status1(:,:), status2(:,:)
  real :: r, epsilon=1e-6, epsilon_sum = 0, epsilon_total
  integer :: etype, subarray_t, order, mode, fh
  integer(MPI_OFFSET_KIND) :: offset

  real, allocatable :: phi(:,:), phi_old(:,:) !do not change to kind=8
  real, allocatable :: f(:,:)

  !derived type for local grid
  !xpe is cartesian coordinate of rank number
  !nnpe are nearest neighbors
  type :: latt_t
      integer :: comm
      integer :: L(dim), N(dim), NPE(dim), xpe(dim), nnpe(-1:1, dim), offset(dim) 
      logical :: periodic(dim)
  end type latt_t
  type(latt_t) :: latt

  call MPI_Init(ierror)
  call MPI_Comm_rank(comm, me, ierror)
  call MPI_Comm_size(comm, npe, ierror)

  if (me == 0) then
     write(*,"(45a)",advance="no") "Please enter the size N (of the NxN matrix): "
     read(*,*) N
  endif
  
  call MPI_Bcast(N, 1, MPI_INTEGER, 0, comm, ierror)

  latt%periodic = (/.false., .false./)
  latt%npe = 0
  !set the grid with available number of processes npe automatically: 12npe -> 4x3 npe
  call MPI_Dims_Create(npe, dim, latt%npe, ierror)

  !set local grid size latt%N
  latt%N = [N,N] / latt%npe

  !in case the user input N is not divisible by process number in x- or y-direction
  !N is calculated new and saved in N_i and N_j respectively. N_i is y-axis and N_j is x-axis.
  N_i = latt%N(1)*latt%npe(1)
  N_j = latt%N(2)*latt%npe(2)

  if (me == 0) then
     print "(a45,i5,a3,i5)", "cartesian grid chosen: ", latt%npe(1), " x ", latt%npe(2)
     print "(a45,i5,a3,i5)", "-> N_i steps in y- and N_j in x-direction: ", N_i, " x ", N_j
     print *, "calculating..."
  endif

  !Create Communicator: ==> latt%comm
  call MPI_Cart_Create(comm, dim, latt%npe, latt%periodic, reorder, latt%comm, ierror)
  !Get cartesian coordinates of process ==> latt%xpe
  call MPI_Cart_Get(latt%comm, dim, latt%npe, latt%periodic, latt%xpe, ierror)
  !Get rank of process
  call MPI_Cart_Rank(latt%comm, latt%xpe, lrank, ierror)

  !calculate bound for local grid
  lower_bound_j = 1+latt%xpe(2) * latt%N(2)
  upper_bound_j = lower_bound_j + latt%N(2) - 1
  lower_bound_i = 1+latt%xpe(1) * latt%N(1)
  upper_bound_i = lower_bound_i + latt%N(1) - 1

  !useful for debugging
  ! print *, lrank, latt%xpe, lower_bound_i, upper_bound_i, lower_bound_j, upper_bound_j
  
  allocate(phi(lower_bound_i:upper_bound_i,lower_bound_j:upper_bound_j), &
           phi_old((lower_bound_i-1):(upper_bound_i+1),(lower_bound_j-1):(upper_bound_j+1)), &
           f(lower_bound_i:upper_bound_i,lower_bound_j:upper_bound_j))
  phi=0.0
  phi_old=0.0
  f=0.0
  
  ! Get neighbors in all directions ==> latt%nnpe
  do d = 1, dim
     latt%nnpe(0,d) = lrank 
     call MPI_Cart_Shift(latt%comm,d-1, 1, latt%nnpe(-1,d),latt%nnpe(1,d),ierror)
  enddo

  !$omp parallel do default(none) shared(f,N_i,N_j,L) &
  !$omp private(i,j,r,lower_bound_j,upper_bound_j, lower_bound_i, upper_bound_i) collapse(2)
  do j=lower_bound_j, upper_bound_j
     do i=lower_bound_i, upper_bound_i
        !x = j/N*L, y=i/N*L therefore we lose the L in the calculation of r 
        r = sqrt((i/real(N_i)-0.5)**2 + (j/real(N_j)-0.5)**2)
        if (r*L .LT. 20 .and. 15 .LT. r*L) then
           f(i,j) = 10
        else if (r*L .LT. 10 .and. 6 .LT. r*L) then
           f(i,j) = -10
        else if (r*L .LT. 2) then
           f(i,j) = 10
        else
           f(i,j) = 0
        endif
        !f(i,j) = me+i
                
     enddo
  enddo
  !$omp end parallel do

  allocate(status1(MPI_STATUS_SIZE,4))
  allocate(status2(MPI_STATUS_SIZE,4))

  !define type for rowwise send
  call MPI_Type_vector(latt%N(2),1,latt%N(1), MPI_REAL, rowtype, ierror)
  call MPI_Type_commit(rowtype, ierror)

  !define type for rowwise receive
  call MPI_Type_vector(latt%N(2),1,latt%N(1)+2, MPI_REAL, rowtype2, ierror)
  call MPI_Type_commit(rowtype2, ierror)   
  

  Iterations: do n_iter=1,200000
     !print *, n_iter
     epsilon_sum = 0
     !$omp parallel do default(none) shared(phi, phi_old, f,lower_bound_j,upper_bound_j,lower_bound_i,upper_bound_i) &
     !$omp private(i,j) reduction(+:epsilon_sum)
     do j=lower_bound_j, upper_bound_j
        do i=lower_bound_i, upper_bound_i
 
           phi(i,j) = 0.25 * (phi_old(i+1,j) + phi_old(i-1,j) + phi_old(i,j+1) + phi_old(i,j-1) - f(i,j))
           
           epsilon_sum = epsilon_sum + (phi(i,j) - phi_old(i,j))**2

        enddo
     enddo
     !$omp end parallel do

     !useful for debugging
     ! print "(i2,1x,a7,i2,/,5(f6.2))", n_iter, "phi_old:", lrank, (phi_old(z,:), z=lower_bound_i-1,upper_bound_i+1)
     ! call MPI_Barrier(comm,ierror)
     ! print "(i2,1x,a7,i2,/,3(f6.2))", n_iter, "phi:",     lrank, (phi(z,:), z=lower_bound_i,upper_bound_i)
     ! call MPI_Barrier(comm,ierror)

     call MPI_Allreduce(epsilon_sum, epsilon_total, 1, MPI_REAL, MPI_SUM, comm, ierror)

     if (sqrt(epsilon_total) < epsilon) then
        if (me == 0) then
           print *, "converged"
           ! print *, epsilon_total
        endif
        exit Iterations
     endif
     
     forall(i=lower_bound_i:upper_bound_i, j=lower_bound_j:upper_bound_j) phi_old(i,j) = phi(i,j)

     !columnwise send of border of phi to bigger phi_old
     call MPI_Isend(phi(lower_bound_i,lower_bound_j),      latt%N(1), MPI_REAL, latt%nnpe(-1,2), tag, comm, request1(1), ierror)
     call MPI_Isend(phi(lower_bound_i,upper_bound_j),      latt%N(1), MPI_REAL, latt%nnpe(1,2),  tag, comm, request1(2), ierror)
     call MPI_Irecv(phi_old(lower_bound_i,lower_bound_j-1),latt%N(1), MPI_REAL, latt%nnpe(-1,2), tag, comm, request1(3), ierror)
     call MPI_Irecv(phi_old(lower_bound_i,upper_bound_j+1),latt%N(1), MPI_REAL, latt%nnpe(1,2),  tag, comm, request1(4), ierror)  

     call MPI_Waitall(4, request1, status1, ierror)

     !rowwise send of border of phi to bigger phi_old
     call MPI_Isend(phi(lower_bound_i,lower_bound_j),        1, rowtype,      latt%nnpe(-1,1), tag2, comm, request2(1), ierror)
     call MPI_Isend(phi(upper_bound_i,lower_bound_j),        1, rowtype,      latt%nnpe(1,1),  tag2, comm, request2(2), ierror)
     call MPI_Irecv(phi_old(lower_bound_i-1,lower_bound_j),  1, rowtype2,     latt%nnpe(-1,1), tag2, comm, request2(3), ierror)
     call MPI_Irecv(phi_old(upper_bound_i+1,lower_bound_j),  1, rowtype2,     latt%nnpe(1,1),  tag2, comm, request2(4), ierror)  

     call MPI_Waitall(4, request2, status2, ierror)     
     
  enddo Iterations
  
  if (me == 0) then
     print *, "writing into file..."
  endif

  !MPI_IO same as in lecture
  latt%offset = latt%xpe * latt%N
  order = MPI_ORDER_FORTRAN; etype = MPI_REAL

  call MPI_Type_create_subarray(dim, [N_i, N_j], latt%N, latt%offset, order, etype, subarray_t, ierror)
  call MPI_Type_commit(subarray_t, ierror)

  !delete file, if it already exists
  INQUIRE(FILE="phi_func_total.bin", EXIST=file_exists)
  if (file_exists .eqv. .true.) then
     call MPI_File_delete("phi_func_total.bin", MPI_INFO_NULL, ierror)
  endif
  
  mode = MPI_MODE_RDWR + MPI_MODE_CREATE
  call MPI_File_open(latt%comm, "phi_func_total.bin", mode, MPI_INFO_NULL, fh, ierror)
  offset = 0
  call MPI_File_set_view(fh, offset, etype, subarray_t, "native", MPI_INFO_NULL, ierror)
  call MPI_File_write_all(fh, phi(lower_bound_i, lower_bound_j), latt%N(1)*latt%N(2), etype, status, ierror)
  call MPI_File_close(fh, ierror)

  call MPI_Finalize(ierror)
  
end program project
