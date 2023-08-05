#!/usr/bin/env python3

"""Module: snapshotter

Handles taking

"""
import datetime
import logging
import os
import threading
import time
import traceback

from .exceptions import ServiceRunnerError
from .logify import Logify
from .slack import SlackAttachment, SlackMessage


__author__ = 'Joe Yennaco'


# Set up logger name for this module
mod_logger = Logify.get_name() + '.service_runner'









class Snapshotter(object):

    def __init__(self, team_id, slacker=None):
        self.cls_logger = mod_logger + '.Snapshotter'
        self.capi = Cons3rtApi()
        self.team_id = team_id
        self.snapshot_drs_list = []
        self.hosts = []
        self.results = []
        self.project_names = []
        self.team_name = None
        self.start_time = None
        self.start_timestamp = None
        self.end_time = None
        self.end_timestamp = None
        self.elapsed_time = None
        self.slacker = slacker

    def get_team_info(self):
        log = logging.getLogger(self.cls_logger + '.get_team_info')
        log.info('Retrieving team info for team ID: {i}'.format(i=str(self.team_id)))
        try:
            team_details = self.capi.get_team_details(team_id=self.team_id)
        except Cons3rtApiError as exc:
            raise SnapshotterError('Problem retrieving team details for team ID: {i}\n{e}'.format(
                i=str(self.team_id), e=str(exc)))
        self.team_name = team_details['name']
        for project in team_details['ownedProjects']:
            self.project_names.append(project['name'])
        log.info('Retrieved details on team [{n}] with ID: {i}'.format(n=self.team_name, i=str(self.team_id)))

    def get_drs(self):
        log = logging.getLogger(self.cls_logger + '.get_drs')
        log.info('Attempting to get a list of DRs in all of the VRs, where the owning project belongs to team'
                 'ID {i}'.format(i=str(self.team_id)))
        try:
            team_drs = self.capi.list_active_runs_in_team(team_id=self.team_id)
        except Cons3rtApiError as exc:
            raise SnapshotterError('Problem retrieving active DRs from team: {i}'.format(i=str(self.team_id))) from exc
        log.info('Found {n} DRs in team ID: {i}'.format(n=str(len(team_drs)), i=str(self.team_id)))

        # Filter on DRs in owned projects
        for team_dr in team_drs:
            if 'id' not in team_dr:
                continue
            if 'project' not in team_dr:
                continue
            if 'name' not in team_dr['project']:
                continue
            if team_dr['project']['name'] in self.project_names:
                log.info('Adding DR {i} in project {p} to the list of DRs to be snapshotted'.format(
                    i=str(team_dr['id']), p=team_dr['project']['name']))
                self.snapshot_drs_list.append(team_dr)
            else:
                log.info('Excluding DR {i} in project {p} to the list of DRs to be snapshotted'.format(
                    i=str(team_dr['id']), p=team_dr['project']['name']))

        # Ensure snapshot DRs were found
        if len(self.snapshot_drs_list) < 1:
            raise SnapshotterError('No DRs found to snapshot')
        log.info('Found {n} DRs to snapshot in projects for team ID: {i}'.format(
            n=str(len(self.snapshot_drs_list)), i=str(self.team_id)))

    def snapshot_drs(self):
        log = logging.getLogger(self.cls_logger + '.snapshot_drs')
        log.info('Attempting to create snapshots from DRs on the snapshot DR list...')
        try:
            results = self.capi.create_run_snapshots_multiple(drs=self.snapshot_drs_list)
        except SnapshotterError as exc:
            msg = 'Problem creating snapshots for runs list'
            raise SnapshotterError(msg) from exc
        for result in results:
            snap = SnapShotterResults(
                host_id=result['host_id'],
                host_role=result['host_role'],
                dr_id=result['dr_id'],
                dr_name=result['dr_name'],
                request_time=result['request_time'],
                result=result['result'],
                error_msg=result['err_msg']
            )
            self.results.append(snap)

    def get_results_str(self):
        res_str = 'DR_ID\tDR_Name\tHostID\tRoleName\tRequestTime\tResult\tError Message\n'
        for result in self.results:
            res_str += \
                str(result.dr_id) + '\t' + \
                result.dr_name + '\t' + \
                str(result.host_id) + '\t' + \
                result.host_role + '\t' + \
                result.request_time + '\t' + \
                result.result + '\t' + \
                result.error_msg + '\n'
        return res_str

    def run(self):
        log = logging.getLogger(self.cls_logger + '.run')
        self.start_time = datetime.datetime.now()
        self.start_timestamp = self.start_time.strftime('%Y%m%d-%H%M%S')
        log.info('Creating snapshots for team ID {i} at: {t}'.format(i=str(self.team_id), t=self.start_time))

        log.info('Retrieving team info, projects, virtualization realms, and runs from team ID: {i}'.format(
            i=str(self.team_id)))
        try:
            self.get_team_info()
            time.sleep(5)
            self.get_drs()
            log.info('Attempting to create snapshots for each DR...')
            self.snapshot_drs()
        except SnapshotterError as exc:
            raise SnapshotterError('Problem retrieving team information for team ID: {i}\n{e}'.format(
                i=str(self.team_id), e=str(exc)))
        self.end_time = datetime.datetime.now()
        self.end_timestamp = self.end_time.strftime('%Y%m%d-%H%M%S')
        self.elapsed_time = self.end_time - self.start_time
        log.info('Completed creating snapshots for team ID {i} at: {t}, total time elapsed: {e}'.format(
            i=str(self.team_id), t=self.end_time, e=str(self.elapsed_time)))
