// Graph props:
//  addr: 10
//  name: inc_by_1
//  trailing_jumps: True

// Predecessors: []
10:
$r1 = 1
goto 50
Exits: [(None, '50')]

// Predecessors: ['10']
50:
$r0 += $r1
return $r0
Exits: []
