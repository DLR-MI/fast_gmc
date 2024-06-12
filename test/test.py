import os
import cv2 as cv
import numpy as np
from fast_gmc import gmc


def test_gmc():
    """Simple test to show how to use GMC and how it performs.
    """
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    prev = cv.imread(os.path.join(curr_dir, 'warp_test_0.jpg'))
    curr = cv.imread(os.path.join(curr_dir, 'warp_test_1.jpg'))

    # Run the actual gmc
    mat = gmc(curr, prev, downscale=4, model='affine')  # or model='homography'

    warped = cv.warpPerspective(curr, mat, (curr.shape[1], curr.shape[0]))

    # Compute the squared error between warped frame and curr frame
    warped_diff = curr.astype(np.float32) - warped.astype(np.float32)
    warped_diff = np.sqrt(warped_diff * warped_diff)
    warped_diff = warped_diff - warped_diff.min(axis=0) / (warped_diff.max(axis=0) - warped_diff.min(axis=0))  # normalize
    # Compute the squared error between previous frame and curr frame
    curr_prev_diff = curr.astype(np.float32) - prev.astype(np.float32)
    curr_prev_diff = np.sqrt(curr_prev_diff * curr_prev_diff)
    curr_prev_diff = curr_prev_diff - curr_prev_diff.min(axis=0) / (curr_prev_diff.max(axis=0) - curr_prev_diff.min(axis=0))  # normalize

    cv.imwrite(os.path.join(curr_dir, 'warped_difference.jpg'), warped_diff)
    cv.imwrite(os.path.join(curr_dir, 'warped_prev_curr.jpg'), curr_prev_diff)

    print("Previous to current frame = {} (RMSE)\nWarped to current frame = {} (RMSE)"
          .format(np.mean(curr_prev_diff), np.mean(warped_diff)))
    print("Transformation matrix:\n{}".format(mat))


if __name__ == '__main__':
    test_gmc()
