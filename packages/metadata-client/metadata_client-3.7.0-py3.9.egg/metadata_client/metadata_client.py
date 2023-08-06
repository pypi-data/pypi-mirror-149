"""MetadataClient class"""

import logging

from .apis import (
    DataFileApi, DataGroupApi, DataGroupRepositoryApi, DataGroupTypeApi,
    DataSourceGroupApi, DataSourceGroupVersionApi, DataTypeApi, ExperimentApi,
    ExperimentTypeApi, InstrumentApi, ParameterApi, ParameterTypeApi,
    DarkRunApi,
    ProposalApi, RepositoryApi, RunApi, SampleApi, UserApi)
# Import common classes
from .common.util import Util
from .modules import (
    DataFile, DataGroup, DataGroupRepository, DataGroupType,
    DataSourceGroup, DataSourceGroupVersion, Experiment,
    Instrument, Parameter, Proposal, Repository, Run, Sample)
from .common.config import DEF_PAGE, DEF_PAGE_SIZE


class MetadataClient(
    DataFileApi, DataGroupApi, DataGroupRepositoryApi, DataGroupTypeApi,
    DataSourceGroupApi, DataSourceGroupVersionApi, DataTypeApi, ExperimentApi,
    ExperimentTypeApi, InstrumentApi, ParameterApi, ParameterTypeApi,
    DarkRunApi, ProposalApi, RepositoryApi, RunApi, SampleApi, UserApi
):
    def get_all_xfel_instruments(self, page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        resp = Instrument.get_all_from_xfel(self, page, page_size)

        if not resp['success']:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)

        return resp

    def get_all_data_group_types(self, page=DEF_PAGE, page_size=DEF_PAGE_SIZE):
        resp = DataGroupType.get_all(self, page, page_size)

        if not resp['success']:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)

        return resp

    def get_active_proposal_by_instrument(self, instrument_id):
        resp = Proposal.get_active_proposal_by_instrument(self, instrument_id)

        if not resp['success']:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)

        return resp

    def get_proposal_info(self, proposal_number, instruments_list):
        logging.debug('proposal_number: {0}'.format(proposal_number))

        # Get PROPOSAL #id from #number
        resp = Proposal.get_by_number_daq_info(self, proposal_number)

        if not resp['success']:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.warning(error_msg)
            return resp

        proposal_id = resp['data']['id']
        proposal_instrument_identifier = resp['data']['instrument_identifier']
        logging.debug('proposal_id: {0}'.format(proposal_id))
        logging.debug('proposal_instrument_identifier: {0}'.format(
            proposal_instrument_identifier))

        # (3) A proposal which belongs to other instrument (e.g. SA3 & HED)
        if instruments_list is not None and \
                proposal_instrument_identifier not in instruments_list:
            ret_msg = "The proposal doesn't match this DAQ instance " \
                      "configured list of allowed instruments!"
            logging.warning(ret_msg)

            resp['info'] = 'Error getting proposal'
            resp['app_info'] = ret_msg
            resp['data'] = {}

        return resp

    def get_repository_by_id(self, repository_id):
        logging.debug('repository_id: {0}'.format(repository_id))

        # Get REPOSITORY #id
        resp = Repository.get_by_id(self, repository_id)

        return resp

    def get_proposal_runs(self, proposal_number,
                          run_number=None, page=DEF_PAGE,
                          page_size=DEF_PAGE_SIZE):
        logging.debug('proposal_number: {0}'.format(proposal_number))

        # Get PROPOSAL #id from #number
        resp = Proposal.get_runs_by_proposal_number(self,
                                                    proposal_number,
                                                    run_number,
                                                    page, page_size)

        number_of_runs = len(resp['data']['runs']) if 'runs' in resp[
            'data'] else 0
        logging.debug('number of runs: {0}'.format(number_of_runs))
        return resp

    def get_proposal_experiments(self, proposal_number):
        logging.debug('proposal_number: {0}'.format(proposal_number))

        # Get PROPOSAL #id from #number
        resp = Proposal.get_by_number(self, proposal_number)
        if not (resp['success'] and resp['data']):
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        proposal_id = resp['data']['id']
        logging.debug('proposal_id: {0}'.format(proposal_id))
        resp = Experiment.get_all_by_proposal_id(self, proposal_id)
        return resp

    def get_proposal_samples(self, proposal_number, page=DEF_PAGE,
                             page_size=DEF_PAGE_SIZE):
        logging.debug('proposal_number: {0}'.format(proposal_number))

        # Get PROPOSAL #id from #number
        resp = Proposal.get_by_number(self, proposal_number)
        if not (resp['success'] and resp['data']):
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        proposal_id = resp['data']['id']
        logging.debug('proposal_id: {0}'.format(proposal_id))
        resp = Sample.get_all_by_proposal_id(self, proposal_id,
                                             page, page_size)
        return resp

    def register_run(self, experiment_id, sample_id,
                     run_dict, data_grp_dict):
        logging.debug('experiment_id: {0}'.format(experiment_id))
        logging.debug('sample_id: {0}'.format(sample_id))
        logging.debug('run_dict: {0}'.format(run_dict))
        logging.debug('data_grp_dict: {0}'.format(data_grp_dict))

        # Validate if Mandatory fields are present
        missing_mandatory = []

        if experiment_id is None:
            missing_mandatory.append('experiment_id')

        run_mandatory_fields = ['run_number', 'begin_at', 'first_train']
        for field in run_mandatory_fields:
            if field not in run_dict:
                missing_mandatory.append('run.{0}'.format(field))

        dgr_mandatory_fields = ['data_group_type_id', 'creator_id',
                                'prefix_path']
        for field in dgr_mandatory_fields:
            if field not in data_grp_dict:
                missing_mandatory.append('data_group.{0}'.format(field))

        if len(missing_mandatory) > 0:
            info_msg = 'The following fields are mandatory: {0}'. \
                format(missing_mandatory)

            return {'info': info_msg,
                    'success': False,
                    'data': {},
                    'app_info': {}}

        resp = self.__create_run_from_dict(experiment_id, sample_id, run_dict)

        if not resp['success']:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        run_id = resp['data']['id']
        logging.debug('run_id: {0}'.format(run_id))

        resp = self.__create_data_group_from_dict(
            experiment_id, run_id, data_grp_dict
        )

        if not resp['success']:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)

            # IMPORTANT: Delete successfully created run
            error_msg = 'Deleting Run with ID: "{0}"'.format(run_id)
            logging.error(error_msg)
            Run.delete_by_id(self, run_id)

            return resp

        data_group_id = resp['data']['id']
        logging.debug('data_group_id: {0}'.format(data_group_id))

        # Build hash information to send back in case of success!
        result_info = {'experiment_id': str(experiment_id),
                       'sample_id': str(sample_id),
                       'run_id': str(run_id),
                       'data_group_id': str(data_group_id)}

        return {'info': 'Run registered successfully',
                'success': True,
                'data': result_info,
                'app_info': {}}

    def register_run_data(self,
                          experiment_id, sample_id,
                          run_id, data_group_id,
                          data_group_dict, data_group_files_ar):
        logging.debug('experiment_id: {0}'.format(experiment_id))
        logging.debug('sample_id: {0}'.format(sample_id))
        logging.debug('run_id: {0}'.format(run_id))
        logging.debug('data_group_id: {0}'.format(data_group_id))
        logging.debug('data_group: {0}'.format(data_group_dict))
        logging.debug('data_group_files: {0}'.format(data_group_files_ar))

        # Validate if Mandatory fields are present
        missing_mandatory = []

        if experiment_id is None:
            missing_mandatory.append('experiment_id')

        if run_id is None:
            missing_mandatory.append('run_id')

        if data_group_id is None:
            missing_mandatory.append('data_group_id')

        if not (data_group_dict is None or data_group_dict == {}):
            dgr_mandatory_fields = ['data_group_type_id',
                                    'creator_id']
            for field in dgr_mandatory_fields:
                if field not in data_group_dict:
                    missing_mandatory.append('data_group.{0}'.format(field))

        if data_group_files_ar is None or data_group_files_ar == []:
            missing_mandatory.append('data_group_files')
        else:
            dgr_files_mandatory_fields = ['filename', 'relative_path']
            for index, file_dict in enumerate(data_group_files_ar):
                for field in dgr_files_mandatory_fields:
                    if field not in file_dict:
                        msg = 'data_group_files[{0}].{1}'.format(index, field)
                        missing_mandatory.append(msg)

        if len(missing_mandatory) > 0:
            info_msg = 'The following fields are mandatory: {0}'. \
                format(missing_mandatory)

            return {'info': info_msg,
                    'success': False,
                    'data': {},
                    'app_info': {}}

        #
        # Update DataGroup information (Optional)
        if not (data_group_dict is None or data_group_dict == {}):
            # Only updates the information, if the hash is received
            resp = DataGroup.update_from_dict(self,
                                              data_group_id, data_group_dict)

            if not resp['success']:
                error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
                logging.error(error_msg)
                return resp

        #
        # CREATE DataFiles from hash
        resp = self.__create_data_file_from_dict(data_group_id,
                                                 data_group_files_ar)

        if not resp['success']:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        data_file_id = resp['data']['id']
        logging.debug('data_file_id: {0}'.format(data_file_id))

        # Build hash information to send back in case of success!
        result_info = {'experiment_id': str(experiment_id),
                       'sample_id': str(sample_id),
                       'run_id': str(run_id),
                       'data_group_id': str(data_group_id),
                       'data_file_id': str(data_file_id)}

        return {'info': 'Run data registered successfully',
                'success': True,
                'data': result_info,
                'app_info': {}}

    def close_run(self,
                  experiment_id, sample_id, run_id, data_group_id,
                  run_dict, dg_params_dict):
        logging.debug('experiment_id: {0}'.format(experiment_id))
        logging.debug('sample_id: {0}'.format(sample_id))
        logging.debug('run_id: {0}'.format(run_id))
        logging.debug('data_group_id: {0}'.format(data_group_id))
        logging.debug('run: {0}'.format(run_dict))
        logging.debug('parameters: {0}'.format(dg_params_dict))

        # Validate if Mandatory fields are present
        missing_mandatory = []

        if str(type(run_dict)) != "<class 'dict'>":
            missing_mandatory.append('run must be a Hash')
        if not (run_dict is None or run_dict == {}):
            run_mandatory_fields = ['end_at', 'last_train']
            for field in run_mandatory_fields:
                if field not in run_dict:
                    msg = 'run.{0}'.format(field)
                    missing_mandatory.append(msg)

        if str(type(dg_params_dict)) != "<class 'dict'>":
            missing_mandatory.append('parameters must be a Hash')
        elif dg_params_dict is None or dg_params_dict == {}:
            # missing_mandatory.append('parameters')
            logging.debug('dg_params_dict is None or {}')
        else:
            dg_parameters_ar = dg_params_dict['parameters']

            if str(type(dg_parameters_ar)) != "<class 'list'>":
                dg_parameters_ar = [{}]

            # {'parameters': []}
            if dg_parameters_ar is None or dg_parameters_ar == []:
                pass

            else:
                dgr_params_mandatory_fields = ['data_source', 'name',
                                               'value', 'minimum', 'maximum',
                                               'mean', 'standard_deviation',
                                               'data_type_id',
                                               'parameter_type_id', 'unit_id']

                for index, parameter_dict in enumerate(dg_parameters_ar):
                    for field in dgr_params_mandatory_fields:
                        if field not in parameter_dict:
                            msg = 'parameters[{0}].{1}'.format(index, field)
                            missing_mandatory.append(msg)

                    # Add relation between data_group and parameters
                    parameter_dict['data_groups_parameters_attributes'] = [
                        {'data_group_id': data_group_id}]

        if len(missing_mandatory) > 0:
            info_msg = 'The following fields are mandatory: {0}'. \
                format(missing_mandatory)

            return {'info': info_msg,
                    'success': False,
                    'data': {},
                    'app_info': {}}

        run_dict['run_id'] = run_id
        run_dict['experiment_id'] = experiment_id
        run_dict['sample_id'] = sample_id

        # Setting up the default value for the flg_status field in close_run
        if 'flg_status' in run_dict:
            run_dict['flg_status'] = Util.get_opt_dict_val(run_dict,
                                                           'flg_status',
                                                           2)
        else:
            # If no flg_status is send, it will be assumed the the run was
            # successfully closed (Closed == 2)
            run_dict['flg_status'] = 2

        # Setting up the default value for the flg_available field in close_run
        if 'flg_available' in run_dict:
            run_dict['flg_available'] = Util.get_opt_dict_val(run_dict,
                                                              'flg_available',
                                                              'true')

        #
        # Update Run information (Optional)
        if not (run_dict is None or run_dict == {}):
            # Only updates the information, if the hash is received

            resp = Run.update_from_dict(self, run_id, run_dict)

            if not resp['success']:
                error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
                logging.error(error_msg)
                return resp

        # CREATE Parameters from hash
        resp = self.__create_parameters_from_dict(dg_params_dict)

        if not resp['success']:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        # data_file_id = resp['data']['id']
        # logging.debug('data_file_id: {0}'.format(data_file_id))
        logging.debug('response data: {0}'.format(resp['data']))

        # Build hash information to send back in case of success!
        result_info = {'experiment_id': str(experiment_id),
                       'sample_id': str(sample_id),
                       'run_id': str(run_id)}

        return {'info': 'Run closed successfully',
                'success': True,
                'data': result_info,
                'app_info': {}}

    def register_run_data_and_results(self,
                                      experiment_id, sample_id,
                                      run_dict, data_group_dict,
                                      data_group_files_ar, dg_params_dict):
        logging.debug('experiment_id: {0}'.format(experiment_id))
        logging.debug('sample_id: {0}'.format(sample_id))
        logging.debug('run_dict: {0}'.format(run_dict))
        logging.debug('data_group_dict: {0}'.format(data_group_dict))
        logging.debug('data_group_files: {0}'.format(data_group_files_ar))
        logging.debug('data_group_parameters: {0}'.format(dg_params_dict))

        #
        # 1. Registers a new run and a new data_group
        result_1 = self.register_run(experiment_id, sample_id,
                                     run_dict, data_group_dict)

        if result_1['success']:
            run_id = result_1['data']['run_id']
            data_group_id = result_1['data']['data_group_id']
        else:
            logging.error(result_1)
            return result_1

        #
        # 2. Registers data_group files only if they exist...
        if data_group_files_ar is None or data_group_files_ar == []:
            logging.debug('No files were generated')
        else:
            result_2 = self.register_run_data(experiment_id,
                                              sample_id,
                                              run_id,
                                              data_group_id,
                                              data_group_dict,
                                              data_group_files_ar)

            if result_2['success']:
                data_file_id = result_2['data']['data_file_id']
            else:
                logging.error(result_2)
                return result_2

        #
        # 3. Closes run and set data_group parameters if they exist...
        result_3 = self.close_run(experiment_id, sample_id,
                                  run_id, data_group_id,
                                  run_dict, dg_params_dict)

        if result_3['success']:
            pass
        else:
            logging.error(result_3)
            return result_3

        # Build hash information to send back in case of success!
        result_info = {'experiment_id': str(experiment_id),
                       'sample_id': str(sample_id),
                       'run_id': str(run_id),
                       'data_group_id': str(data_group_id),
                       'data_file_id': str(data_file_id)}

        return {'info': 'Run closed successfully',
                'success': True,
                'data': result_info,
                'app_info': {}}

    def register_run_replica(self,
                             proposal_number, run_number,
                             repository_identifier):
        replica_registration = True

        resp = self.__manage_run_replica(
            proposal_number, run_number, repository_identifier,
            replica_registration
        )
        return resp

    def get_run_register_repositories(self,
                                      proposal_number, run_number,
                                      repository_identifier):
        replica_registration = False

        resp = self.__manage_run_replica(
            proposal_number, run_number, repository_identifier,
            replica_registration
        )
        return resp

    def unregister_run_replica(self,
                               proposal_number, run_number,
                               repository_identifier):
        replica_registration = False

        resp = self.__manage_run_replica(
            proposal_number, run_number, repository_identifier,
            replica_registration
        )
        return resp

    def search_data_files(self, run_number, proposal_number):
        resp = DataFile.search_data_files(self, run_number, proposal_number)

        if not resp['success']:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        return {'info': 'Search data files return successfully',
                'success': True,
                'data': resp['data'],
                'app_info': {}}

    def get_data_source_group(self, data_source_group_name):
        resp = DataSourceGroup.get_by_name(self, data_source_group_name)
        if not resp['success']:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)

        return resp

    def get_data_source_group_version(self, data_source_group_id,
                                      version_name):
        resp = DataSourceGroupVersion.get(self, data_source_group_id,
                                          version_name)
        if not resp['success']:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)

        return resp

    def update_data_source_group_version(self, id, params):
        resp = DataSourceGroupVersion.update(self, id, params)
        if not resp['success']:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)

        return resp

    def get_data_source_group_version_by_name(self, group_name, version_name):
        # getting Data source group
        resp = self.get_data_source_group(group_name)
        if not resp['success'] or len(resp['data']) == 0:
            return
        dsg = resp['data'][0]

        # getting Data source group version
        resp = self.get_data_source_group_version(dsg['id'], version_name)
        if not resp['success'] or len(resp['data']) == 0:
            return
        return resp['data'][0]

    def deploy_data_source_group_version(self, group_name, version_name):
        dsgv = self.get_data_source_group_version_by_name(group_name,
                                                          version_name)
        if not dsgv:
            return {'info': 'DSG version not found',
                    'success': False,
                    'data': {},
                    'app_info': {}}

        if dsgv['flg_status'] == DataSourceGroupVersion.FLG_STATUS_DEPLOYED:
            return {
                'info':
                    'DSG version already marked as deployed. Nothing to do.',
                'success': True,
                'data': {},
                'app_info': {}}

        # Mark version as deployed
        resp = self.update_data_source_group_version(dsgv['id'], {
            'last_deployed_at': None,
            'flg_status': DataSourceGroupVersion.FLG_STATUS_DEPLOYED
        })
        if not resp['success']:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        return {'info': 'DSG version deployed successfully',
                'success': True,
                'data': {},
                'app_info': {}}

    def __create_run_from_dict(self,
                               experiment_id, sample_id, run_dict):
        logging.debug('experiment_id: {0}'.format(experiment_id))
        logging.debug('sample_id: {0}'.format(sample_id))
        logging.debug('run: {0}'.format(run_dict))

        run_experiment_id = str(experiment_id)

        # Handles the situation when sample_id isn't specified
        run_sample_id = Util.get_opt_val(sample_id)

        run_run_number = run_dict['run_number']  # Mandatory
        run_run_alias = Util.get_opt_dict_val(run_dict, 'run_alias')
        run_begin_at = run_dict['begin_at']  # Mandatory
        run_end_at = Util.get_opt_dict_val(run_dict, 'end_at')
        run_first_train = Util.get_opt_dict_val(run_dict, 'first_train')
        run_last_train = Util.get_opt_dict_val(run_dict, 'last_train')
        run_flg_avail = Util.get_opt_dict_val(run_dict,
                                              'flg_available', 'true')
        run_flg_status = Util.get_opt_dict_val(run_dict, 'flg_status', '1')
        run_orig_format = Util.get_opt_dict_val(run_dict, 'original_format')
        run_sys_msg = Util.get_opt_dict_val(run_dict, 'system_msg')
        run_desc = Util.get_opt_dict_val(run_dict, 'description')

        mdc_run = {
            'run_number': run_run_number,
            'run_alias': run_run_alias,
            'experiment_id': run_experiment_id,
            'sample_id': run_sample_id,
            'begin_at': run_begin_at,
            'end_at': run_end_at,
            'first_train': run_first_train,
            'last_train': run_last_train,
            'flg_available': run_flg_avail,
            'flg_status': run_flg_status,
            'original_format': run_orig_format,
            'system_msg': run_sys_msg,
            'description': run_desc
        }
        logging.debug('Built Run: {0}'.format(mdc_run))

        #
        # Create Run from dictionary
        #
        return Run.create_from_dict(self, mdc_run)

    def __create_data_group_from_dict(self, experiment_id,
                                      run_id, dgrp_dict):
        logging.debug('experiment_id: {0}'.format(experiment_id))
        logging.debug('run_id: {0}'.format(run_id))
        logging.debug('data_group: {0}'.format(dgrp_dict))

        #
        dgr_name = Util.get_opt_dict_val(dgrp_dict, 'name')
        dgr_lang = Util.get_opt_dict_val(dgrp_dict, 'language', 'en')
        dgr_doi = Util.get_opt_dict_val(dgrp_dict, 'doi')
        dgr_type_id = dgrp_dict['data_group_type_id']  # Mandatory
        dgr_exp_id = experiment_id  # Mandatory
        dgr_creator_id = dgrp_dict['creator_id']  # Mandatory
        dgr_prefix_path = dgrp_dict['prefix_path']  # Mandatory
        dgr_flg_avail = Util.get_opt_dict_val(dgrp_dict, 'flg_available',
                                              'true')
        dgr_flg_writing = Util.get_opt_dict_val(dgrp_dict, 'flg_writing',
                                                'false')
        dgr_flg_pub = Util.get_opt_dict_val(dgrp_dict, 'flg_public', 'false')
        dgr_format = Util.get_opt_dict_val(dgrp_dict, 'format')
        dgr_data_passport = Util.get_opt_dict_val(dgrp_dict, 'data_passport')
        dgr_removed_at = Util.get_opt_dict_val(dgrp_dict, 'removed_at')
        dgr_desc = Util.get_opt_dict_val(dgrp_dict, 'description')

        mdc_data_group = {
            'name': dgr_name,
            'language': dgr_lang,
            'doi': dgr_doi,
            'data_group_type_id': dgr_type_id,
            'experiment_id': dgr_exp_id,
            'user_id': dgr_creator_id,
            'prefix_path': dgr_prefix_path,
            'flg_available': dgr_flg_avail,
            'flg_writing': dgr_flg_writing,
            'flg_public': dgr_flg_pub,
            'format': dgr_format,
            'data_passport': dgr_data_passport,
            'removed_at': dgr_removed_at,
            'description': dgr_desc,
            'runs_data_groups_attributes': [{
                'run_id': run_id}]
        }
        logging.debug('Built DataGroup: {0}'.format(mdc_data_group))

        return DataGroup.create_from_dict(self, mdc_data_group)

    def __create_data_file_from_dict(self, data_group_id, files_list):
        logging.debug('data_group_id: {0}'.format(data_group_id))
        logging.debug('data_group_files: {0}'.format(files_list))

        data_file_group_id = data_group_id
        data_file_files = str(files_list).replace(' ', '')

        mdc_data_file = {
            'data_group_id': data_file_group_id,
            'files': data_file_files
        }
        logging.debug('Built DataFile: {0}'.format(mdc_data_file))

        return DataFile.create_from_dict(self, mdc_data_file)

    def __create_parameters_from_dict(self, parameters_list):
        logging.debug('parameters: {0}'.format(parameters_list))

        return Parameter.create_multiple_from_dict(self, parameters_list)

    def __set_data_group_repo_from_dict(self, data_group_id,
                                        repository_id, flg_available):
        logging.debug('data_group_id: {0}'.format(data_group_id))
        logging.debug('repository_id: {0}'.format(repository_id))
        logging.debug('flg_available: {0}'.format(flg_available))

        data_group_repository = {
            'data_group_id': data_group_id,
            'repository_id': repository_id,
            'flg_available': flg_available
        }
        msg = 'Built DataGroupRepository: {0}'.format(data_group_repository)
        logging.debug(msg)

        return DataGroupRepository.set_from_dict(self, data_group_repository)

    def __manage_run_replica(self,
                             proposal_number, run_number,
                             repository_identifier, replica_registration):
        if replica_registration:
            flg_available = 'true'
            info_msg = 'Run replica registered successfully'
        else:
            flg_available = 'false'
            info_msg = 'Run replica unregistered successfully'

        # 1. Get repository_id from repository_identifier
        resp = Repository.get_all_by_identifier(self, repository_identifier)

        if not resp['success']:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        repository_id = resp['data'][0]['id']

        # 2. Get all data_groups from current run_number
        resp = Run.get_all_raw_data_groups(self, run_number, proposal_number)

        if not resp['success']:
            error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
            logging.error(error_msg)
            return resp

        data_group_ids = resp['data']

        result_info_all = []
        for data_group_id in data_group_ids:
            # 3. Register the data group replica
            # CREATE DataGroupRepository registry from hash
            resp = self.__set_data_group_repo_from_dict(
                data_group_id, repository_id, flg_available
            )

            if not resp['success']:
                error_msg = '{0} >> {1}'.format(resp['info'], resp['app_info'])
                logging.error(error_msg)
                return resp

            # Build hash information to send back in case of success!
            result_info = {'data_group_id': str(data_group_id),
                           'repository_id': str(repository_id),
                           'flg_available': str(flg_available)}

            result_info_all.append(result_info)

        return {'info': info_msg,
                'success': True,
                'data': result_info_all,
                'app_info': {}}
