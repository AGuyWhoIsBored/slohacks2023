<script lang="ts">
	export let data;

	// state for class entry
	let enteredClasses = '';
	$: formattedClasses = enteredClasses.split('\n').filter((entry) => entry.length);

	// state for curriculum sheet selection
	let selectedCurriculumSheet = '';

	// state for input validation
	$: validInput = selectedCurriculumSheet !== '' && formattedClasses.length > 0;

	$: console.log('ssr data', data);
	$: console.log('formattedclasses', formattedClasses);
	$: console.log('selectedsheet', selectedCurriculumSheet);
	$: console.log('validinput', validInput);

	let statusText = 'Status: Not Yet Run';
	let resParsed: any[] | null = null;

	$: console.log('resparsed', resParsed);

	$: {
		resParsed;

		if (resParsed) {
			statusText = `Status: Validation ${resParsed.length > 0 ? 'FAILURE' : 'SUCCESS'}`;
		}
	}

	async function submitCurriculumValidationTask() {
		const res: string = await fetch('http://localhost:8080/curriculum', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				CurriculumName: selectedCurriculumSheet,
				Classes: formattedClasses
			})
		}).then((resp) => resp.json());

		// res will be a string at this point, convert to json
		resParsed = JSON.parse(res.replace(/'/g, '"'));
	}
</script>

<div class="appContainer m-4">
	<div class="card cardStyles h-full">
		<div class="card-body">
			<div>
				<h1 class="text-3xl font-medium inline-block">Cal Poly Curriculum Sheet Validator</h1>
				<img
					class="inline-block ml-2 mb-2"
					src="/logo.png"
					width="32"
					height="32"
					alt="horse thing"
				/>
			</div>

			<div class="flex justify-between">
				<p class="flex-grow-0">How does this work? It doesn't</p>
				<p class="flex-grow-0">
					Duncan Applegarth, Mitchell Kanazawa, Wesley Kwok (SLO Hacks 2023)
				</p>
			</div>

			<div class="flex flex-grow">
				<div class="grid flex-grow grid-flow-col grid-cols-2">
					<div class="border-r-2">
						<div>
							<h2 class="text-center text-2xl font-medium mt-4">Enter Classes Here</h2>
							<div class="divider mx-8 h-0" />
						</div>
						<textarea
							class="w-[96%] mx-4 h-72 resize-none border-2"
							placeholder="Enter your courses here, one on each line"
							bind:value={enteredClasses}
						/>

						<div class="mt-6">
							<h2 class="text-center text-2xl font-medium mt-4">Select Curriculum Sheet</h2>
							<div class="divider mx-8 h-0" />
						</div>

						<select
							class="w-[96%] mx-4 select select-sm select-bordered"
							bind:value={selectedCurriculumSheet}
						>
							<option selected disabled value="">Select a Curriculum Sheet ...</option>
							{#each data.curriculums as curriculum}
								<option value={curriculum}>{curriculum}</option>
							{/each}
						</select>

						<div class="mt-40">
							{#if formattedClasses.length === 0}
								<p class="ml-4 text-sm text-red-500">
									Please enter a list of courses before submitting.
								</p>
							{:else}
								<!-- nice -->
								<p class="ml-4 text-sm text-white">all good!</p>
							{/if}

							{#if selectedCurriculumSheet === ''}
								<p class="ml-4 text-sm text-red-500">
									Please select a curriculum sheet before submitting.
								</p>
							{:else}
								<p class="ml-4 text-sm text-white">all good!</p>
							{/if}
							<button
								disabled={!validInput}
								class="w-[96%] mx-4 btn btn-success text-white mt-4"
								on:click={submitCurriculumValidationTask}>Submit</button
							>
						</div>
					</div>

					<div>
						<div>
							<h2 class="text-center text-2xl font-medium mt-4">Validation Results</h2>
							<div class="divider mx-8 h-0" />
						</div>

						<h3 class="ml-4 text-lg">{statusText}</h3>

						{#if resParsed && resParsed.length > 0}
							<div class="ml-4 mt-8">
								<h3>Missing Requirements:</h3>
								<ol class="ml-8">
									{#each resParsed as entry}
										<li class="list-decimal">{entry.join(', ')}</li>
									{/each}
								</ol>
							</div>
						{/if}
					</div>
				</div>
			</div>
		</div>
	</div>
</div>

<style lang="postcss">
	.appContainer {
		/* got lazy */
		height: calc(100vh - 32px);
	}

	.cardStyles {
		@apply shadow border-base-300 rounded-sm;

		/* make shadow a hair darker */
		--tw-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.2), 0 1px 2px 0 rgba(0, 0, 0, 0.16);
	}
</style>
