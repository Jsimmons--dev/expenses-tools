import argparse
import sys
import queue
import io
import json


class CLI(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="cli tool for analyzing expenses",
            usage='''python -m tax/calc <command> [<args>]

takeHome
            ''')
        parser.add_argument('command', help='sub command to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    def takeHome(self):
        parser = argparse.ArgumentParser(
            description="remove common windows background patterns from an isolated event document"
        )
        parser.add_argument(
            '--bracketFile', help="The tax brackets to calculate with", default="tax/2019brackets.json"
        )
        parser.add_argument(
            '--fileStatus', help="The filing status to use e.g. married single", default="single"
        )
        parser.add_argument(
            '--gross', help="The gross salary that you would like to calculate take home for", type=int
        )

        args = parser.parse_args(sys.argv[2:])

        if args.gross == None:
            parser.print_help()
            exit(1)

        with open(args.bracketFile) as f:
            bracketJson = json.load(f)
            brackets = bracketJson[args.fileStatus]
            taxAmount = 0
            leftOver = args.gross
            for bracket in brackets:
                # print("left over is: %s" % str(leftOver))
                if leftOver > 0:
                    if len(bracket['range']) < 2:
                        # print('last bracket')
                        taxAmount += bracket['rate'] * leftOver
                        break
                    if leftOver >= bracket['range'][1] - bracket['range'][0]:
                        # print('full bucket left: %s and range is %s' %
                            #   (leftOver, bracket['range']))
                        leftOver -= bracket['range'][1] - bracket['range'][0]
                        taxAmount += (bracket['range'][1] -
                                      bracket['range'][0]) * bracket['rate']
                    else:
                        # print('empty the rest')
                        taxAmount += leftOver * bracket['rate']
                        leftOver = 0
                        break
            print("gross: %s, taxed amount: %s, after tax: %s, effective tax rate: %s" % (args.gross, taxAmount, args.gross - taxAmount,
                                                                                          1 - ((args.gross - taxAmount) / args.gross)))


if __name__ == '__main__':
    CLI()
