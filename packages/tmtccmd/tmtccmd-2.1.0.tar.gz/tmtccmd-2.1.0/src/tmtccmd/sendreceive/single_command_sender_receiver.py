#!/usr/bin/python3.8
"""
@file
    tmtcc_config.py
@date
    01.11.2019
@brief
    Used to send single tcs and listen for replies after that
"""
from tmtccmd.ccsds.handler import CcsdsTmHandler
from tmtccmd.sendreceive.cmd_sender_receiver import CommandSenderReceiver
from tmtccmd.sendreceive.tm_listener import TmListener

from tmtccmd.com_if.com_interface_base import CommunicationInterface

from tmtccmd.utility.tmtc_printer import FsfwTmTcPrinter
from tmtccmd.logging import get_console_logger

from tmtccmd.tc.definitions import PusTcTupleT


logger = get_console_logger()


class SingleCommandSenderReceiver(CommandSenderReceiver):
    """
    Specific implementation of CommandSenderReceiver to send a single telecommand
    This object can be used by instantiating it and calling sendSingleTcAndReceiveTm()
    """

    def __init__(
        self,
        com_if: CommunicationInterface,
        tmtc_printer: FsfwTmTcPrinter,
        tm_listener: TmListener,
        tm_handler: CcsdsTmHandler,
        apid: int,
    ):
        """
        :param com_if: CommunicationInterface object, passed on to CommandSenderReceiver
        :param tm_listener: TmListener object which runs in the background and receives all TM
        :param tmtc_printer: TmTcPrinter object, passed on to CommandSenderReceiver
        """
        super().__init__(
            com_if=com_if,
            tm_listener=tm_listener,
            tmtc_printer=tmtc_printer,
            tm_handler=tm_handler,
            apid=apid,
        )

    def send_single_tc_and_receive_tm(self, pus_packet_tuple: PusTcTupleT):
        """
        Send a single telecommand passed to the class and wait for replies
        :return:
        """
        try:
            pus_packet_raw, pus_packet_obj = pus_packet_tuple
        except TypeError:
            logger.error("SingleCommandSenderReceiver: Invalid command input")
            return
        self._operation_pending = True
        self._tm_listener.set_listener_mode(TmListener.ListenerModes.SEQUENCE)
        self._tmtc_printer.print_telecommand(
            tc_packet_obj=pus_packet_obj, tc_packet_raw=pus_packet_raw
        )
        self._com_if.send(data=pus_packet_raw)
        self._last_tc = pus_packet_raw
        self._last_tc_obj = pus_packet_obj
        while self._operation_pending:
            # wait until reply is received
            super()._check_for_first_reply()
        if self._reply_received:
            self._tm_listener.set_mode_op_finished()
            packet_queue = self._tm_listener.retrieve_ccsds_tm_packet_queue(
                apid=self._apid, clear=True
            )
            self._tm_handler.handle_ccsds_packet_queue(
                apid=self._apid, packet_queue=packet_queue
            )
            logger.info("SingleCommandSenderReceiver: Reply received")
            logger.info("Listening for packages ...")
