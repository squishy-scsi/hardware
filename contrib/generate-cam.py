#!/usr/bin/env python

import json

from pathlib    import Path
from subprocess import run, PIPE
from argparse   import ArgumentParser
from sys        import exit
from shutil     import which
from zipfile    import ZipFile

KICAD_CLI = Path(which('kicad-cli')).resolve()

def run_command(args: tuple[str, ...]) -> tuple[int, str, str]:
	ret = run((KICAD_CLI, *args), stderr = PIPE, stdout = PIPE)
	return (
		ret.returncode, ret.stderr.decode('utf-8'), ret.stdout.decode('utf-8')
	)

def sch_cam(basename: str, schematic: Path, outdir: Path, do_check: bool = False, allow_check_fail: bool = False) -> int:
	print(f'Generating schematic CAD/CAM files from \'{schematic.name}\'')
	report_file = (outdir / f'{basename}-erc.json')
	bom_file    = (outdir / f'{basename}-bom.csv')
	pdf_file    = (outdir / f'{basename}.pdf')

	if do_check:
		print(f'\tRunning ERC on \'{schematic.name}\'')
		ret, stderr, stdout = run_command((
			'sch', 'erc', '-o', report_file,
			'--format', 'json', '--exit-code-violations', '--severity-all',
			schematic
		))
		print(f'\tERC Report: \'{report_file}\'')

		with report_file.open('r') as rpt:
			erc_report = json.load(rpt)

		violations = tuple(
			v
			for vs in map(lambda sheet: list(map(lambda violations: violations['severity'] if not violations.get('excluded', False) else None, sheet['violations'])), erc_report['sheets'])
			for v in vs
		)

		exl_count = violations.count(None)
		err_count = violations.count('error')
		wrn_count = violations.count('warning')

		if exl_count > 0:
			print('\t\tExclusions:')
			print(f'\t\t\tFound {exl_count} excluded ERC violations')

		if wrn_count > 0:
			print('\t\tWarnings:')
			print(f'\t\t\tFound {wrn_count} ERC warnings!')

		if err_count > 0:
			print('\t\tErrors:')
			print(f'\t\t\tFound {err_count} ERC violations!')
			if not allow_check_fail:
				return 1
			else:
				print('\tWARNING: ERC Failed but continuing to generate CAD/CAM Files!')
		else:
			print('\t\tERC Clean')

	# Generate the BOM
	print(f'\tGenerating Bill-of-Materials: \'{bom_file}\'')
	ret, stdout, stderr = run_command((
		'sch', 'export', 'bom', '-o', bom_file,
		'--fields', 'Reference,Value,Tolerance,${QUANTITY},MFR,MPN,SUPPLIER_OC,SUPPLIER_URL',
		schematic
	))

	if ret != 0:
		print('\tGenerating Bill-of-Materials failed!')
		print(stdout)
		print(stderr)
		return 1

	# Generate the schematic PDF
	print(f'\tGenerating rendered schematic: \'{pdf_file}\'')
	ret, stdout, stderr = run_command((
		'sch', 'export', 'pdf', '-o', pdf_file, schematic
	))

	if ret != 0:
		print('\tGenerating rendered schematic failed!')
		print(stdout)
		print(stderr)
		return 1

	print('Schematic CAD/CAM generation done')
	return 0

def pcb_cam(basename: str, pcb: Path, outdir: Path, do_check: bool = False, allow_check_fail: bool = False) -> int:
	print(f'Generating PCB CAD/CAM files from \'{pcb.name}\'')
	report_file     = (outdir / f'{basename}-drc.json')
	gerber_dir      = (outdir / 'gerbers')
	gerber_zip_file = (outdir / f'{basename}-gerbers.zip')
	ptop_file       = (outdir / f'{basename}-top-pos.csv')
	pbot_file       = (outdir / f'{basename}-bot-pos.csv')

	gerber_dir.mkdir(exist_ok = True)

	if do_check:
		print(f'\tRunning DRC on \'{pcb.name}\'')
		ret, stderr, stdout = run_command((
			'pcb', 'drc', '-o', report_file,
			'--format', 'json', '--exit-code-violations', '--severity-all', '--schematic-parity',
			pcb
		))
		print(f'\tDRC Report: \'{report_file}\'')

		with report_file.open('r') as rpt:
			drc_report = json.load(rpt)

		violations = tuple(map(lambda violations: violations['severity'] if not violations.get('excluded', False) else None, drc_report['violations']))
		schem_parity = tuple(map(lambda violations: violations['severity'] if not violations.get('excluded', False) else None, drc_report['schematic_parity']))
		unconnected = tuple(map(lambda violations: violations['severity'] if not violations.get('excluded', False) else None, drc_report['unconnected_items']))


		exl_count = violations.count(None)
		err_count = violations.count('error')
		wrn_count = violations.count('warning')

		sch_excl = schem_parity.count(None)
		sch_errs = schem_parity.count('error')
		sch_wrns = schem_parity.count('warning')

		ucon_excl = unconnected.count(None)
		ucon_errs = unconnected.count('error')
		ucon_wrns = unconnected.count('warning')

		if (exl_count + sch_excl + ucon_excl) > 0:
			print('\t\tExclusions:')
			print(f'\t\t\tFound {exl_count} excluded DRC violations')
			print(f'\t\t\tFound {sch_excl} excluded DRC warnings')
			print(f'\t\t\tFound {ucon_excl} excluded unconnected items')

		if (wrn_count + sch_wrns + ucon_wrns) > 0:
			print('\t\tWarnings:')
			print(f'\t\t\tFound {wrn_count} DRC warnings!')
			print(f'\t\t\tFound {sch_wrns} Schematic parity warnings!')
			print(f'\t\t\tFound {ucon_wrns} Unconnected Item warnings!')

		if (err_count + sch_errs + ucon_errs) > 0:
			print('\t\tErrors:')
			print(f'\t\t\tFound {err_count} DRC violations!')
			print(f'\t\t\tFound {sch_errs} Schematic parity errors!')
			print(f'\t\t\tFound {ucon_errs} Unconnected Item errors!')

			if not allow_check_fail:
				return 1
			else:
				print('\tWARNING: DRC Failed but continuing to generate CAD/CAM Files!')
		else:
			print('\t\tDRC Clean')

	# Generate the Gerber files
	print(f'\tGenerating Gerbers: \'{gerber_dir}\'')

	ret, stdout, stderr = run_command((
		'pcb', 'export', 'gerbers', '-o', gerber_dir,
		'--use-drill-file-origin', '--no-x2', '--subtract-soldermask',
		'-l', 'F.Cu,B.Cu,In1.Cu,In2.Cu,In3.Cu,In4.Cu,In5.Cu,In6.Cu,Edge.Cuts,F.Fab,B.Fab,F.Mask,B.Mask,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen',
		pcb
	))

	# Remove the grbjob file
	grbjob = (gerber_dir / f'{basename}-job.gbrjob')
	if grbjob.exists():
		grbjob.unlink()

	if ret != 0:
		print('\tGenerating Gerbers failed!')
		print(stdout)
		print(stderr)
		return 1

	# Generate the Drill files
	print(f'\tGenerating Drills: \'{gerber_dir}\'')

	ret, stdout, stderr = run_command((
		'pcb', 'export', 'drill', '-o', gerber_dir,
		'--format', 'excellon', '--drill-origin', 'plot',
		pcb
	))

	if ret != 0:
		print('\tGenerating Drills failed!')
		print(stdout)
		print(stderr)
		return 1

	# Archive Gerbers / Drill files
	print(f'\tGenerating Gerber/Drill Archive: \'{gerber_zip_file}\'')

	if gerber_zip_file.exists():
		gerber_zip_file.unlink()

	with ZipFile(gerber_zip_file, 'w') as gerb_zip:
		for gf in gerber_dir.iterdir():
			gerb_zip.write(gf, gf.name)

	# Generate the PnP file: top
	print(f'\tGenerating PnP File: \'{ptop_file}\'')

	ret, stdout, stderr = run_command((
		'pcb', 'export', 'pos', '-o', ptop_file,
		'--format', 'csv', '--side', 'front',
		pcb
	))

	if ret != 0:
		print('\tGenerating PnP File failed!')
		print(stdout)
		print(stderr)
		return 1

	# Generate the PnP file: bot
	print(f'\tGenerating PnP File: \'{pbot_file}\'')

	ret, stdout, stderr = run_command((
		'pcb', 'export', 'pos', '-o', ptop_file,
		'--format', 'csv', '--side', 'back',
		pcb
	))

	if ret != 0:
		print('\tGenerating PnP File failed!')
		print(stdout)
		print(stderr)
		return 1

	print('Schematic CAD/CAM generation done')

	return 0

def main() -> int:

	parser = ArgumentParser(
		__file__,
		description = 'Generate CAM files'
	)

	parser.add_argument(
		'--output', '-o',
		type     = Path,
		required = True,
		help     = 'Output Directory for CAM generation'
	)

	parser.add_argument(
		'--input', '-i',
		type     = Path,
		required = True,
		help     = 'Input directory containing KiCad source files'
	)

	parser.add_argument(
		'--run-checks', '-r',
		action  = 'store_true',
		default = False,
		help    = 'Run ERC and DRC before generating the CAM output files'
	)

	parser.add_argument(
		'--allow-failures', '-F',
		action  = 'store_true',
		default = False,
		help    = 'Continue generating CAD and CAM output even if ERC/DRC checks fail'
	)

	args = parser.parse_args()

	outdir: Path = args.output
	indir: Path = args.input

	if not KICAD_CLI.exists():
		print('ERROR: Unable to find `kicad-cli`!')
		return 1

	if not indir.exists():
		print(f'ERROR: No such directory {indir}!')
		return 1

	kicad_project = next(indir.glob('*.kicad_pro')).resolve()
	project_name = kicad_project.stem

	print(f'Found KiCad project: {kicad_project.name}')

	root_sch = (indir / f'{project_name}.kicad_sch').resolve()
	root_pcb = (indir / f'{project_name}.kicad_pcb').resolve()

	if not root_sch.exists():
		print(f'ERROR: Root SCH file {root_sch} does not exist!')
		return 1
	print(f'Root SCH: {root_sch}')


	if not root_pcb.exists():
		print(f'ERROR: Root PCB file {root_pcb} does not exist!')
		return 1
	print(f'Root PCB: {root_pcb}')

	cam_dir = (outdir / project_name)

	if not cam_dir.exists():
		cam_dir.mkdir(parents = True)

	sch_ret = sch_cam(project_name, root_sch, cam_dir, args.run_checks, args.allow_failures)
	pcb_ret = pcb_cam(project_name, root_pcb, cam_dir, args.run_checks, args.allow_failures)


	return (sch_ret | pcb_ret)


if __name__ == '__main__':
	exit(main())
