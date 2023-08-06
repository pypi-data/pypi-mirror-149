from logging import getLogger
import re

logger = getLogger()


def search_pattern(pattern: str, target: str):
    """
    Search pattern including numbers from target.

    >>> _search_pattern('1.~19.丁目', '11.丁目')
    True
    """
    ranges = []
    re_pattern = pattern
    for m in re.finditer(r'((\d+)\.)?(~((\d+)\.)?)?', pattern):
        if m.group(0) == '':
            continue

        span = m.group(0)
        args = m.groups()
        logger.debug('args:{}'.format(m.groups()))
        if args[1] is None and args[4] is None:
            continue

        while len(args) < 5:
            args.append(None)

        re_pattern = re_pattern.replace(span, r'(\d+)\.')
        if args[4]:
            if args[1] is None:
                ranges.append([None, int(args[4])])
            else:
                ranges.append([int(args[1]), int(args[4])])
        elif args[2]:
            ranges.append([int(args[1]), None])
        else:
            ranges.append([int(args[1]), int(args[1])])

    logger.debug('re_pattern: "{}"'.format(re_pattern))
    logger.debug(ranges)

    m = re.search(re_pattern, target)
    if m is None:
        logger.debug('not match at all.')
        return False

    for i, val in enumerate(m.groups()):
        v = int(val)
        r = ranges[i]
        logger.debug('Comparing value {} to range {}'.format(
            v, r))
        if r[0] is not None and v < r[0]:
            logger.debug('  {} is smaller than {} (FAIL)'.format(
                v, r[0]))
            return False

        if r[1] is not None and v > r[1]:
            logger.debug('  {} is larget than {} (FAIL)'.format(
                v, r[1]))

    logger.debug('Pass all check.')
    return True


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)

    search_pattern('第9.地割~第11.地割', '第10.地割')
    search_pattern('第9.~11.地割', '第10.地割')
    # search_pattern('1.~19.丁目', '11.丁目')
    # search_pattern('北', '北六丁目')
    # search_pattern('8.丁目', '5.丁目')
