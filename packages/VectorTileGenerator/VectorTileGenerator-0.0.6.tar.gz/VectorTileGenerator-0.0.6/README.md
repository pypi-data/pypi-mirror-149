# VectorTileGenerator

A python package to automatically generate a list of all possible z,x,y tiles options between two zoom levels and a bounding box.

## Install
`pip install VectorTileGenerator`

## How to use
```
from VectorTileGenerator import generator
import json

tileGeneration = generator.GenerateTiles(1, 3, [-118, 34, -84, 50])

# Demo of generating tiles
print(json.dumps(tileGeneration.generate(), indent=4))

{
    "1": [
        [
            1,
            0,
            0
        ]
    ],
    "2": [
        [
            2,
            0,
            1
        ],
        [
            2,
            1,
            1
        ]
    ],
    "3": [
        [
            3,
            1,
            2
        ],
        [
            3,
            1,
            3
        ],
        [
            3,
            2,
            2
        ],
        [
            3,
            2,
            3
        ]
    ]
}
```