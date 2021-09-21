# Duplicate Image Detection

## Getting Started

- Install dependencies `pip install -r requirements.txt`
- Run service `python main.py`

### Testing

- Test with `pytest`

## How it Works

![alt text](./docs/sys-design.png 'Duplicate image detection system')

This system uses a perceptual hashing function, similar to Apple's CSAM Detection. Instead of generating image hashes using NeuralHash, it uses a difference hash (dHash), which is simpler and less computationally intensive as it doesn't require neural networks. Since we don't have the same privacy constraints as Apple, we will be using nearest neighbor searches to identify duplicate images.

### Difference Hash

dHash is a perceptual hashing function that produces hash values that are resilient to image scaling, as well as changes in color, brightness, and aspect ratio [1]. There are 4 main steps for creating a difference hash for an image:

![alt text](./docs/dhash-steps.png 'dHash procedure')

1. Convert to greyscale\*
2. Resize image to (hash_size+1, hash_size)
3. Calculate horizontal gradient, reducing image size to (hash_size, hash_size)
4. Assign bits based on horizontal gradient values

\*We convert the image to greyscale before resizing for optimal performance

### Nearest Neighbors

Image hashes that we want to check for duplicates against will be stored in a binary index for fast and efficient nearest neighbor searches. We will use Hamming distance as a metric to determine the similarity between image hashes, for dHash, distances less than 10 (96.09% similarity) likely indicate similar/duplicate images [1].

# References

[1] https://www.hackerfactor.com/blog/?/archives/529-Kind-of-Like-That.html
