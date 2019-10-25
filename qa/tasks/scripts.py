import os

from util import copy_directory_recursively


class Scripts:

    def __init__(self, ctx, logger):
        self.log = logger
        copied = ctx.get('scripts_copied', False)
        remotes = ctx['remotes']
        if copied:
            # self.log.info('(scripts ctor) scripts already copied to remotes')
            pass
        else:
            local_path = os.path.dirname(os.path.realpath(__file__)) + '/scripts/'
            for remote_name, remote_obj in remotes.items():
                copy_directory_recursively(local_path, remote_obj, "scripts")
            ctx['scripts_copied'] = True

    def run(self, remote, script_name, args=[], as_root=True):
        """
        Note: args should be as simple as possible, and not contain quotation
        marks. Sorry that's kinda lame.
        """
        class_name = type(remote).__name__
        self.log.debug(
            '(scripts) run method was passed a remote object of class {}'
            .format(class_name)
            )
        if class_name == 'Cluster':
            remote_spec = 'the whole cluster'
        else:
            remote_spec = 'remote {}'.format(remote.hostname)
        self.log.info('(scripts) running script {} with args {} on {}'
                      .format(script_name, args, remote_spec)
                      )
        cmd = 'scripts/' + script_name
        if args:
            cmd += ' '.join(map(str, args))
        cmd = "bash -c '{}'".format(cmd)
        if as_root:
            cmd = "sudo {}".format(cmd)
        return remote.sh(cmd, label=script_name)
