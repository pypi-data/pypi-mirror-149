"""All the pricing."""

import tensorflow as tf

from tensorflow import math


def _is_whole(line):
    """1 if the line is 'whole' else 0"""

    return tf.equal(math.mod(line, 4), 0)


def asian_market_pricer(probs, line, probs_offset=0, batch_dims=0):
    """Asian handicap market pricer"""

    # Make it so when we divide by 4 below we are actually calculating (line / 4 + probs_offset)
    ix = line + probs_offset * 4

    lt_ix = math.floordiv(ix - 2, 4)
    half_lt_ix = math.floordiv(ix - 1, 4)
    half_gt_ix = math.floordiv(ix + 1, 4)

    cdf = tf.cumsum(probs, axis=-1)

    lt_prob = tf.gather(cdf, lt_ix, axis=-1, batch_dims=batch_dims)

    non_zero_half_lt_prob = tf.gather(probs, half_lt_ix, axis=-1, batch_dims=batch_dims)
    half_lt_prob = tf.where(_is_whole(line - 1), non_zero_half_lt_prob, 0.0)

    non_zero_half_gt_prob = tf.gather(probs, half_gt_ix, axis=-1, batch_dims=batch_dims)
    half_gt_prob = tf.where(_is_whole(line + 1), non_zero_half_gt_prob, 0.0)

    gt_prob = 1.0 - tf.gather(cdf, half_gt_ix, axis=-1, batch_dims=batch_dims)

    gt_price = 1.0 + (lt_prob + 0.5 * half_lt_prob) / (gt_prob + 0.5 * half_gt_prob)
    lt_price = 1.0 + (gt_prob + 0.5 * half_gt_prob) / (lt_prob + 0.5 * half_lt_prob)

    return gt_price, lt_price


def one_x_two_pricer(probs, probs_offset):
    """1x2 market pricer"""

    pmf_offset_p1 = probs_offset + 1

    team2_win_prob = tf.reduce_sum(probs[..., :probs_offset], axis=-1)
    draw_prob = probs[..., probs_offset]
    team1_win_prob = tf.reduce_sum(probs[..., pmf_offset_p1:], axis=-1)

    return (
        math.reciprocal(team1_win_prob),
        math.reciprocal(draw_prob),
        math.reciprocal(team2_win_prob),
    )
